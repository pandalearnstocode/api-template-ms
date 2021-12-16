import argparse
import getpass
import hashlib
import os
import pathlib
import shutil
import subprocess
import traceback
from functools import partial
from typing import List

import pandas as pd
from azure.storage.blob import BlobServiceClient
from azure.storage.blob._blob_client import BlobClient
from compression import decompress_file
from joblib import Parallel, delayed
from loguru import logger
from settings import BLOB_CONTAINER, CONNECTION_STRING, MAX_LOG_SIZE

base_dir = pathlib.Path(__file__).parent  # / "data"

DF_LOGS = None


# util function to display bytes
def _strfbytes(bytes_value: int, unit: str = None, decimal_points: int = 2) -> str:
    def get_memory_units(unit=None, p=None):
        if unit is None:
            if p == 0:
                unit = "B"
            elif p == 1:
                unit = "KB"
            elif p == 2:
                unit = "MB"
            elif p == 3:
                unit = "GB"
            elif p == 4:
                unit == "TB"
            else:
                unit = ""

            return unit
        if p is None:
            if unit == "B":
                p = 0
            elif unit == "KB":
                p = 1
            elif unit == "MB":
                p = 2
            elif unit == "GB":
                p = 3
            elif unit == "TB":
                p = 4
            else:
                assert "Can't support unit greater than TB"
            return p

    converted = float(bytes_value)
    if unit is None:
        p = 0
        while bytes_value > 1024:
            converted /= 1024.0
            if converted < 0.5:
                converted *= 1024.0
                break
            p += 1
        unit = get_memory_units(p=p)
        converted = round(converted, decimal_points)
    else:
        p = get_memory_units(unit=unit)
        converted = round(converted / (1024.0 ^ p), decimal_points)
    return f"{str(converted)} {unit}"


# Checks if the file exists
def _does_file_exist(
    file_in_dir: pathlib.Path, blob_file: BlobClient, files_downloaded: set, chunk_size: int = 4096,
) -> bool:
    properties = blob_file.get_blob_properties()
    # check if file exists in dir
    if file_in_dir not in files_downloaded:
        return False

    # comparing blob and dir file size (bytes)
    if file_in_dir.stat().st_size != properties.size:
        return False

    # comparing the data inside using hash
    blob_hex_val = properties.content_settings.content_md5.hex()
    md5_hash = hashlib.md5()
    with open(file_in_dir, "rb") as handle:
        for byte_block in iter(partial(handle.read, chunk_size), b""):
            md5_hash.update(byte_block)
    return blob_hex_val == md5_hash.hexdigest()


# Load Hash log from file
def _load_hash_log(log_file: pathlib.Path = base_dir / "hash_log.csv"):
    global DF_LOGS
    if log_file.is_file():
        DF_LOGS = pd.read_csv(log_file, parse_dates=["log_datetime"])
        logger.info("Hash log loaded!")
    else:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        DF_LOGS = pd.DataFrame(
            columns=["log_datetime", "hash_key", "blob_name", "size", "user_name", "forced", "dvc_skipped",]
        )
        logger.info("Hash logs not found, creating new hash log!")


def _create_log_frame(
    hash_val: str, blob_name: str, file_size: int, force: bool, skip_dvc: bool,
):
    return {
        "log_datetime": pd.to_datetime("today"),
        "hash_key": hash_val,
        "blob_name": blob_name,
        "size": file_size,
        "user_name": getpass.getuser(),
        "forced": force,
        "dvc_skipped": skip_dvc,
    }


# Update the hash values in log
def _update_hash_log(logs: List[dict], log_file: pathlib.Path = base_dir / "hash_log.csv"):
    global DF_LOGS
    # forced to loop since parallel returns None during skip
    for log in logs:
        if log is not None:
            DF_LOGS = DF_LOGS.append(log, ignore_index=True)
    DF_LOGS.sort_values(by="log_datetime", ascending=False).loc[:MAX_LOG_SIZE].to_csv(log_file, index=False)
    logger.info("Hash files saved!")


# Check if file is downloaded using hash_log
def _check_hash_log(hash_val: str) -> bool:
    global DF_LOGS
    return any(DF_LOGS["hash_key"] == hash_val)


def _save_blob_file(
    blob, container_client, files_downloaded, raw_file_dir, extract_2_dir, force, keep, skip_dvc, need_dvc,
):
    blob_client = container_client.get_blob_client(blob.name)
    properties = blob_client.get_blob_properties()
    path = raw_file_dir.joinpath(blob.name).absolute()
    blob_split = blob.name.rsplit("/", 1)
    hex_val = blob_split[1].split("_", 1)[0]  # hash-val_actual_filename.ext

    extract_to = extract_2_dir / blob_split[0] / blob_split[1].split("_", 1)[1]
    file_exists = _does_file_exist(path, blob_client, files_downloaded)

    if force or (not _check_hash_log(hex_val) and not file_exists):
        logger.info(
            f"""Downloading {blob.name} - Last Modified:
            {str(blob.last_modified)}
            Size: {_strfbytes(properties.size)}
            md5: {hex_val} in {path.parent.absolute()}\n"""
        )
        path.parent.mkdir(parents=True, exist_ok=True)

        with path.open("wb") as my_blob:
            download_stream = blob_client.download_blob()
            my_blob.write(download_stream.readall())
        files_downloaded.add(path)
        logger.info(f"{blob.name} Download complete!\n")
        logger.info(f"Decompressing {blob.name}!\n")
        new_file = decompress_file(
            path, extract_to=extract_to.parent, new_file_name=extract_to.stem, delete_compressed=not keep,
        )
        if new_file is not None:
            need_dvc.add(new_file.with_suffix(new_file.suffix))
            return _create_log_frame(hex_val, blob.name, properties.size, force, skip_dvc,)
    elif not _check_hash_log(hex_val) and file_exists:  # file wasn't extracted!
        logger.info(f"Decompressing {blob.name}!\n")
        new_file = decompress_file(
            path, extract_to=extract_to.parent, new_file_name=extract_to.stem, delete_compressed=not keep,
        )
        if new_file is not None:
            need_dvc.add(new_file.with_suffix(new_file.suffix))
            return _create_log_frame(hex_val, blob.name, properties.size, force, skip_dvc,)
    else:
        need_dvc.add((extract_to.parent / (extract_to.stem)))
        logger.info(f"Skipping {blob.name}!\n")


def blob_download(
    base_dir, raw_file_dir, extract_2_dir, files_downloaded, force=False, keep=False, skip_dvc=False, n_jobs=10,
):
    """Downloads all blobs in the container to the raw_file_dir."""
    n_downloads = 0
    need_dvc = set()
    blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
    container_client = blob_service_client.get_container_client(BLOB_CONTAINER)

    blobs_list = container_client.list_blobs()
    logs = Parallel(n_jobs=n_jobs, prefer="threads")(
        delayed(_save_blob_file)(
            blob, container_client, files_downloaded, raw_file_dir, extract_2_dir, force, keep, skip_dvc, need_dvc,
        )
        for blob in blobs_list
    )
    _update_hash_log(logs=logs, log_file=base_dir / "hash_log.csv")
    if not keep and raw_file_dir.exists():
        shutil.rmtree(raw_file_dir)  # delete the entire folder and subfolders

    return n_downloads, need_dvc


def dvc_update(
    base_dir, update_dvc: bool = False, auto_commit: bool = False, need_dvc: List[pathlib.Path] = None,
):
    """Updates the dvc repo with the files in need_dvc."""
    env = os.environ.copy()
    # add dvc to extracted files
    if update_dvc or need_dvc is None:
        path_glob = base_dir.glob("*/raw/*")
        need_dvc = set(x for x in path_glob if x.is_file())

    exts = set("".join(f.suffixes) for f in need_dvc if f.suffix != ".dvc")

    try:
        # new files added, include in dvc. Warning the new dvc files are not committed!
        for ext in exts:
            glob_path = base_dir.relative_to(base_dir.parent).as_posix() + f"/*/raw/*{ext}"
            subprocess.run(f'dvc add "{glob_path}" --glob', shell=True, env=env)

        subprocess.run("dvc diff", shell=True, env=env)

        subprocess.run("dvc push", shell=True, env=env)

        if auto_commit:
            subprocess.run("git add *.dvc", shell=True, env=env)
            subprocess.run(
                f"git commit -m \"DVC files updated {pd.to_datetime('today')}\"", shell=True, env=env,
            )
            logger.info("DVC files commited!")
        logger.info("DVC files updated!")
        return True
    except Exception as e:
        logger.error(f"Error occured during DVC tracker update!\n{repr(e)}\n{traceback.format_exc()}")
        return False


def get_data(
    base_dir: pathlib.Path = base_dir,
    raw_file_dir: pathlib.Path = None,
    extract_2_dir: pathlib.Path = None,
    force: bool = False,
    keep: bool = False,
    update_dvc: bool = False,
    skip_dvc: bool = False,
    auto_commit: bool = False,
    n_jobs=10,
):
    """Downloads all blobs in the container to the raw_file_dir."""
    # fixme: check if dvc and its required modules are installed

    if not isinstance(base_dir, pathlib.Path):
        base_dir = pathlib.Path(base_dir)
    logger.info(f"Working base directory {base_dir.absolute()}")
    # Check current downloaded dvc files
    if raw_file_dir is None:
        raw_file_dir = base_dir / "raw"  # / "data" / "raw"
    elif not isinstance(raw_file_dir, pathlib.Path):
        raw_file_dir = pathlib.Path(raw_file_dir)

    if extract_2_dir is None:
        extract_2_dir = base_dir
    elif not isinstance(extract_2_dir, pathlib.Path):
        extract_2_dir = pathlib.Path(extract_2_dir)

    path_glob = raw_file_dir.glob("**/*")
    files_downloaded = set(x for x in path_glob if x.is_file())
    need_dvc = None
    _load_hash_log(base_dir / "hash_log.csv")
    if not update_dvc:
        logger.info(
            f"{('No' if len(files_downloaded) == 0 else f'Currently {len(files_downloaded)}' )} files downloaded!"
        )
        n_downloads, need_dvc = blob_download(
            base_dir, raw_file_dir, extract_2_dir, files_downloaded, force, keep, skip_dvc, n_jobs,
        )

    if not update_dvc and skip_dvc:
        logger.warning("DVC tracking skipped by user! This might cause issues!\n")
        logger.info(f"{len(files_downloaded)} Existing Downloads, {n_downloads} New files Downloaded\n")
    else:
        status_update = dvc_update(base_dir, update_dvc, auto_commit, need_dvc)
        if status_update is False:
            logger.error("DVC Update Failed!")
        elif update_dvc:
            logger.info("DVC files updated!")
        else:
            logger.info(f"{len(files_downloaded)} files Downloaded, {n_downloads} New files Downloaded.")

    logger.info("Data synchronization complete!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser("For downloading files from azure blob to data directory")

    parser.add_argument("--force", action="store_true", help="Replace all files and update dvc trackers")
    parser.add_argument("--keep", action="store_true", help="Keep the downloaded raw files")
    parser.add_argument(
        "--update-dvc", action="store_true", help="Skips download and only updates the DVC files",
    )
    parser.add_argument(
        "--skip-dvc",
        action="store_true",
        help="Skips DVC trackers for the new downloaded files. Warning this can cause issues.",
    )
    parser.add_argument(
        "-b", "--base-dir", type=str, default=None, help="The absolute base directory for data",
    )
    parser.add_argument(
        "-r",
        "--raw-file-dir",
        type=str,
        default=None,
        help="The absolute path directory to store raw files from azure blob",
    )
    parser.add_argument(
        "-e",
        "--extract_2_dir",
        type=str,
        default=None,
        help="The destination path directory for azure blob files to be extracted",
    )
    parser.add_argument(
        "-n",
        "--n_jobs",
        type=int,
        default=10,
        help="The destination path directory for azure blob files to be extracted",
    )
    parser.add_argument("-c", "--auto-commit", action="store_true", help="Enable DVC files auto commit")

    args = parser.parse_args()
    get_data(
        base_dir if args.base_dir is None else pathlib.Path(args.base_dir),
        args.raw_file_dir,
        args.extract_2_dir,
        args.force,
        args.keep,
        args.update_dvc,
        args.skip_dvc,
        args.auto_commit,
        args.n_jobs,
    )

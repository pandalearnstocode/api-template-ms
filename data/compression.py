import bz2
import os
import pathlib
import pickle

import _pickle as cPickle
import pandas as pd
from loguru import logger


def save_file(file_name, data):
    """Save data to a file."""
    with bz2.BZ2File(file_name, "wb") as f:
        cPickle.dump(data, f)
    return file_name


def compress_files():
    """Compress all files in data."""
    files_path = []
    for path, subdirs, files in os.walk("."):
        for name in files:
            files_path.append(pathlib.PurePath(path, name))
    csv_files = []
    pickle_files = []
    for file in files_path:
        if file.endswith((".csv")):
            csv_files.append(file)
        if file.endswith((".pickle", ".pkl")):
            pickle_files.append(file)

    if csv_files:
        for csv_file in csv_files:
            df = pd.read_csv(csv_file)
            df.to_csv(csv_file + ".gzip", compression="gzip", index=None)

    if pickle_files:
        for pickle_file in pickle_files:
            with open(pickle_file, "rb") as handle:
                data = pickle.load(handle)
                save_file(pickle_file + ".pbz2", data)


def decompress_files():
    """Decompress all files in data."""
    files_path = []
    for path, subdirs, files in os.walk("."):
        for name in files:
            files_path.append(pathlib.PurePath(path, name))
    zipped_csv_files = []
    zipped_pickle_files = []
    for file in files_path:
        if str(file).endswith((".gzip")):
            zipped_csv_files.append(file)
        if str(file).endswith((".pbz2")):
            zipped_pickle_files.append(file)

    if zipped_csv_files:
        for csv_file in zipped_csv_files:
            df = pd.read_csv(csv_file, compression="gzip")
            df.to_csv(str(csv_file).replace(".gzip", ""), index=None)
            if os.path.isfile(csv_file):
                os.remove(csv_file)
            else:  # Show an error
                logger.error(f"Error: {csv_file} file not found")

    if zipped_pickle_files:
        for pickle_file in zipped_pickle_files:
            data = bz2.BZ2File(pickle_file, "rb")
            data = cPickle.load(data)
            with open(str(pickle_file).replace(".pbz2", ""), "wb") as handle:
                pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
            if os.path.isfile(pickle_file):
                os.remove(pickle_file)
            else:  # Show an error ##
                logger.error(f"Error: {pickle_file} file not found")


def decompress_file(
    file: pathlib.Path,
    extract_to: pathlib.Path = None,
    new_file_name: str = None,
    delete_compressed: bool = True,
) -> pathlib.Path:
    """Decompresses the given file.

    Args:
        file (pathlib.Path): File required to decompress
        extract_to (pathlib.Path, optional): The path directory destination for the extracted files. Defaults to None.
        new_file_name (str, optional): The new file name after extraction. Defaults to None.
        delete_compressed (bool, optional): Delete compressed files after extraction. Defaults to True.

    Returns:
        pathlib.Path: returns the extracted path.
    """
    if not file.is_file():
        return None
    if file.suffix == ".gzip":
        df = pd.read_csv(file, compression="gzip")
        save_as = file.parent if extract_to is None else extract_to
        save_as.mkdir(parents=True, exist_ok=True)
        save_as = save_as / (file.stem if new_file_name is None else new_file_name)
        if save_as.exists():
            save_as.unlink()
        df.to_csv(save_as, index=None)
    elif file.suffix == ".pbz2":
        data = bz2.BZ2File(file, "rb")
        data = cPickle.load(data)
        save_as = file.parent if extract_to is None else extract_to
        save_as.mkdir(parents=True, exist_ok=True)
        save_as = save_as / (file.stem if new_file_name is None else new_file_name)
        if save_as.exists():
            save_as.unlink()
        with open(save_as, "wb") as handle:
            pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
    else:  # file not supported
        return None
    logger.info(f"Extracted to {save_as}")
    if delete_compressed:
        if file.is_file():
            file.unlink()
        else:
            logger.error(f"Error: {file} file not found")
    return save_as

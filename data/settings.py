import os

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())


CONNECTION_STRING = os.getenv("CONNECTION_STRING")
BLOB_CONTAINER = os.getenv("BLOB_CONTAINER")
MAX_LOG_SIZE = int(os.getenv("MAX_LOG_SIZE", "30"))

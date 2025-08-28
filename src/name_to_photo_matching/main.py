import traceback
import argparse

from .clip_functions import CLIPHandler
from .utils import to_csv
from .gcs import CloudStorageHandler
from loguru import logger


def main():
    try:
        logger.info("Initializing main workflow...")
        client = CloudStorageHandler("cults_files",
                                     "cloud_storage_service_account.json")

        file_name_map = client.get_3mfs_and_parse_file_names()
        to_csv(file_name_map, "current_cults_files.csv")
        client.download_bucket(destination_directory="~/sba/name_to_photo_matching/photos")

    except Exception as e:
        traceback.print_exc()
        logger.error(f"Main workflow failed: {e}")


if __name__ == "__main__":
    main()

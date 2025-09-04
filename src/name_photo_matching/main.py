import traceback
import click

from .clip_functions import CLIPHandler
from .utils import to_csv
from .gcs import CloudStorageHandler
from loguru import logger
from typing import Optional


def init(bucket: str, service_account_path: Optional[str] = None):
    logger.info("Creating GCS client instance.")
    if service_account_path:
        logger.info("Using service account to create credentials")
        try:
            client = CloudStorageHandler(bucket, service_account_path)

            return client

        except Exception as e:
            traceback.print_exc()
            logger.error(f"Creating credentials with service account failed: {e}")

    else:
        from google.cloud import storage
        logger.info("Service account path was not passed. Using Google ADC instead.")

        try:
            client = storage.Client()
            return client

        except Exception as e:
            traceback.print_exc()
            logger.error(f"Creating credentials with Google ADC failed {e}")

def main():
    try:
        logger.info("Initializing main workflow...")
        client = init_gcs_client()

        file_name_map = client.get_3mfs_and_parse_file_names()
        to_csv(file_name_map, "current_cults_files.csv")
        client.download_bucket(destination_directory="~/sba/name_to_photo_matching/photos")

    except Exception as e:
        traceback.print_exc()
        logger.error(f"Main workflow failed: {e}")


if __name__ == "__main__":
    app()

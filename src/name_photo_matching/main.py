import traceback

from .clip_functions import CLIPHandler
from .utils import to_csv
from .gcs import CloudStorageHandler
from loguru import logger
from typing import Optional

import argparse


def init_gcs_client(bucket: str, service_account_path: Optional[str] = None):
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
    parser = argparse.ArgumentParser(
        prog="Shoebutton Artistry CLI",
        description="CLI tools to assist with management and automation of product uploads and merchandising for Shoebutton Artistry"
    )

    subparsers = parser.add_subparsers(dest="command")
    storage_parser = subparsers.add_parser("storage")
    storage_subparsers = storage_parser.add_subparsers(dest="subcommand", required=True)
    storage_init_parser = storage_subparsers.add_parser("init", help="Initialize storage")
    storage_init_parser.add_argument("service_account_file", help="Path to service account JSON")
    storage_init_parser.add_argument("bucket", help="Bucket to access")
    storage_file_parser = storage_subparsers.add_parser("files", help="Get current files in storage")


    args = parser.parse_args()

    if args.command == "storage":
        if args.subcommand == "init":
            client = init_gcs_client(args.bucket, args.service_account_file)

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

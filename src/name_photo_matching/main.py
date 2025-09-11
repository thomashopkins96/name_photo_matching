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


def build_parser():
    parser = argparse.ArgumentParser(
        prog="Shoebutton Artistry CLI",
        description="CLI tools to assist with management and automation of product uploads and merchandising for Shoebutton Artistry"
    )

    subparsers = parser.add_subparsers(dest="command")
    auth_parser = subparsers.add_parser("auth")
    auth_subparsers = auth_parser.add_subparsers(dest="subcommand", required=True)
    auth_init_parser = auth_subparsers.add_parser("init", help="Verify Google credentials")
    auth_init_parser.add_argument("service_account_file", help="Path to service account JSON")
    storage_parser = subparsers.add_parser("storage")
    storage_subparsers = storage_parser.add_subparsers(dest="subcommand", required=True)

    storage_files_parser = storage_subparsers.add_parser("files")
    storage_files_subparser = storage_files_parser.add_subparsers(dest="subcommand", required=True)

    storage_list_parser = storage_files_subparser.add_parser("list", help="List current files")
    storage_list_parser.add_argument("--bucket", required=True, help="Bucket to access")
    storage_list_parser.add_argument("--output", help="Format for output")

    storage_download_parser = storage_files_subparser.add_parser("download", help="Download files from bucket")
    storage_download_parser.add_argument("--bucket", required=True, help="Bucket to access")
    storage_download_parser.add_argument("--destination", help="Destination folder for downloaded content")

    similarity_parser = subparsers.add_parser("similarity")
    similarity_subparsers = similarity_parser.add_subparsers(dest="subdommand", required=True)
    similarity_encode_parser = similarity_subparsers.add_parser("encode", help="Command to encode an input to embeddings")
    similarity_encode_image_subparser = similarity_encode_parser.add_subparsers(dest="subcommand", required=True)
    similarity_encode_image_parser = similarity_encode_image_subparser.add_parser("images", help="Encode images")
    similarity_encode_text_parser = similarity_encode_image_subparser.add_parser("text", help="Encode text")

    similarity_encode_image_parser.add_argument("directory", required=True)
    similarity_encode_text_parser.add_argument("directory", required=True)

    return parser

def main():
    args = parser.parse_args()

    if args.command == "auth":
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

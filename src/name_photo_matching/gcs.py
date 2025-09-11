from google.cloud import storage
import re
import traceback
from loguru import logger
import os


class CloudStorageHandler:
    def __init__(self, bucket: str, service_account_path: str):
        self.bucket = bucket

        try:
            logger.info("Verifying Google Cloud Storage client via service account...")
            self.client = storage.Client.from_service_account_json(service_account_path)

            logger.success("Successfully initialized client!")

        except Exception as e:
            traceback.print_exc()
            logger.error(f"Client verification failed: {e}")

    def get_bucket_name(self):
        return self.bucket

    def get_3mfs_and_parse_file_names(self):
        results = {
                "original_file_name": [],
                "parsed_file_name": []
        }
        regex_for_3mfs = r"(?:cults_files/)?(?:freshie_mold)?([^.]*)\.3mf.*"
        logger.info(f"Using {regex_for_3mfs} to find 3mf files.")

        try:
            file_names = self.client.list_blobs(self.bucket)

            for file in file_names:
                results['original_file_name'].append(file.id)
                parsed_file_name = re.sub(regex_for_3mfs, lambda m: m.group(1)
                    .replace("_", " ")
                    .replace(" freshie mold", ""), file.id)

                results['parsed_file_name'].append(parsed_file_name)

            return results

        except Exception as e:
            traceback.print_exc()
            logger.error(f"Pulling and parsing file names failed: {e}")

    def download_bucket(self,
                        max_workers: int = 8,
                        destination_directory: str = ""):
        from google.cloud.storage import transfer_manager

        try:
            bucket_obj = self.client.bucket(self.bucket)

            blob_names = [
    blob.name for blob in bucket_obj.list_blobs(max_results=1000)
            ]
            if os.path.isdir(destination_directory):
                results = transfer_manager.download_many_to_path(
                    bucket_obj,
                    blob_names,
                    destination_directory=destination_directory,
                    max_workers=max_workers)

                for name, result in zip(blob_names, results):
                    if isinstance(result, Exception):
                        print("Failed to download {} due to exception: {}"
                              .format(name, result))
                    else:
                        print("Downloaded {} to {}."
                              .format(name, destination_directory + name))

            else:
                traceback.print_exc()
                logger.error("Directory passed in destination_directory does not exist.")

        except Exception as e:
            traceback.print_exc()
            logger.error(f"Failed to download files from bucket {self.get_bucket_name()} because of error: {e}")

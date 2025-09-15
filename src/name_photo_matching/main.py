from .cli_functions import CultsProducts
from .gcs import CloudStorageHandler
import argparse


def cmd_auth_init(args):
    # Just prove we can auth (optionally list 1 blob)
    h = CloudStorageHandler(bucket=args.bucket, service_account_path=args.service_account_file)
    # Try a tiny call to confirm permissions:
    try:
        blobs = h.list_bucket_files(prefix=args.prefix, delimiter=args.delimiter)
        first = next(iter(blobs), None)
        if first:
            print(f"Authenticated. Sample object: {getattr(first, 'name', getattr(first, 'id', 'unknown'))}")
        else:
            print("Authenticated. Bucket is reachable but empty (or prefix had no matches).")
    except StopIteration:
        print("Authenticated. No objects found.")
    return 0

def cmd_storage_files_list(args):
    print(f"[storage:files:list] bucket={args.bucket} output={args.output}")


def cmd_storage_files_download(args):
    print(f"[storage:files:download] bucket={args.bucket} prefix={args.prefix!r} dst={args.destination!r}")


def cmd_similarity_encode_images(args):
    print(f"[similarity:encode:images] dir={args.directory}")


def cmd_similarity_encode_text(args):
    print(f"[similarity:encode:text] dir={args.directory}")


def build_parser():
    parser = argparse.ArgumentParser(
        prog="Shoebutton Artistry CLI",
        description="CLI tools to assist with management and automation of product uploads and merchandising for Shoebutton Artistry",
    )

    main_sub = parser.add_subparsers(dest="command", required=True)

    # auth
    auth = main_sub.add_parser("auth", help="Authentication")
    auth_sub = auth.add_subparsers(dest="auth_cmd", required=True)

    auth_init = auth_sub.add_parser("init", help="Verify Google credentials")
    auth_init.add_argument("service_account_file", help="Path to service account JSON")
    auth_init.add_argument("--bucket", help="Optional bucket to test access")
    auth_init.set_defaults(func=cmd_auth_init)

    # storage
    storage = main_sub.add_parser("storage", help="Google Cloud Storage operations")
    storage_sub = storage.add_subparsers(dest="storage_cmd", required=True)

    files = storage_sub.add_parser("files", help="Work with objects in a bucket")
    files_sub = files.add_subparsers(dest="files_cmd", required=True)

    files_list = files_sub.add_parser("list", help="List current files")
    files_list.add_argument("--bucket", required=True, help="Bucket to access")
    files_list.add_argument("--output", choices=["table", "json", "csv"], default="table", help="Output format")
    files_list.add_argument("--prefix", default="", help="Only list keys with this prefix")
    files_list.set_defaults(func=cmd_storage_files_list)

    files_dl = files_sub.add_parser("download", help="Download files from bucket")
    files_dl.add_argument("--bucket", required=True, help="Bucket to access")
    files_dl.add_argument("--prefix", default="", help="Only download keys with this prefix")
    files_dl.add_argument("--destination", default=".", help="Destination folder")
    files_dl.set_defaults(func=cmd_storage_files_download)

    # similarity
    similarity = main_sub.add_parser("similarity", help="Embedding / similarity utilities")
    sim_sub = similarity.add_subparsers(dest="similarity_cmd", required=True)

    encode = sim_sub.add_parser("encode", help="Encode inputs to embeddings")
    encode_sub = encode.add_subparsers(dest="modality", required=True)

    enc_imgs = encode_sub.add_parser("images", help="Encode images in a directory")
    enc_imgs.add_argument("directory", help="Directory of images")
    enc_imgs.set_defaults(func=cmd_similarity_encode_images)

    enc_text = encode_sub.add_parser("text", help="Encode text files in a directory")
    enc_text.add_argument("directory", help="Directory of text files")
    enc_text.set_defaults(func=cmd_similarity_encode_text)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    if hasattr(args, "func"):
        return args.func(args)
    # Fallback (shouldn't hit because subparsers are required):
    parser.print_help()

if __name__ == "__main__":
    app()

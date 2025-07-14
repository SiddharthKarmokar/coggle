import argparse
from pathlib import Path
from coggle.core.injector import inject_logger
from coggle.core.auth import install_kaggle_json
from coggle.exceptions import KaggleAuthError
from coggle.core.kaggle_runner import push_kernel, download_outputs, build_kernel_metadata
from coggle.utils import wait_for_kernel_to_finish
from coggle.core.drive_sync import sync_artifacts_to_drive, authenticate_drive, download_artifacts_from_drive
from kaggle import api
import os

def run_coggle(args):
    
    entry_path = Path(args.entry)
    project_dir = entry_path.parent

    if not entry_path.exists():
        print(f"[coggle] Error: Entry file does not exist: {entry_path}")
        return

    inject_logger(str(entry_path))

    username = api.get_config_value("username") or os.getenv("KAGGLE_USERNAME")  # Replace with dynamic load later
    slug = project_dir.name.replace(" ", "-").lower()
    metadata = build_kernel_metadata(username, slug, entry_path.name, args.title, private=True, gpu=args.gpu)
    metadata_path = project_dir / "kernel-metadata.json"
    metadata.save(str(metadata_path))

    try:
        push_kernel(str(project_dir))
    except KaggleAuthError as e:
        print(str(e))
        return

    # 4. Download output (optional)
    if args.download:
        if wait_for_kernel_to_finish(f"{username}/{slug}"):
            download_outputs(f"{username}/{slug}", args.output)
        else:
            print("[Warning] Kernel didn't finish. Skipping output download.")

    if not args.no_sync:
        sync_artifacts_to_drive(args.drive_folder)


def main():
    parser = argparse.ArgumentParser(prog="coggle", description="Run and manage Kaggle notebook workflows")

    subparsers = parser.add_subparsers(dest="command")
    auth_parser = subparsers.add_parser("auth", help="Install kaggle.json for Kaggle CLI")
    run_parser = subparsers.add_parser("run", help="Run and push code to Kaggle")
    drive_parser = subparsers.add_parser("drive-auth", help="Authenticate to Google Drive using PyDrive2")
    download_parser = subparsers.add_parser("download-drive", help="Download artifacts from Google Drive")

    # coggle run
    download_parser.add_argument("--folder-name", type=str, default="coggle-artifacts", help="Drive folder name to download from")
    download_parser.add_argument("--target", type=str, default="artifacts", help="Local directory to store downloads")
    auth_parser.add_argument("--file", required=True, help="Path to kaggle.json")
    run_parser.add_argument("--entry", type=str, required=True, help="Path to your main entry file (e.g. input/main.py)")
    run_parser.add_argument("--output", type=str, default="output", help="Output directory for results/logs")
    run_parser.add_argument("--artifacts", type=str, default="artifacts", help="Artifacts folder to sync to Drive")
    run_parser.add_argument("--gpu", action="store_true", help="Enable GPU on Kaggle")
    run_parser.add_argument("--title", type=str, help="Title of the Kaggle kernel")
    run_parser.add_argument("--drive-folder", type=str, default="coggle-artifacts", help="Google Drive folder to upload to")
    run_parser.add_argument("--no-sync", action="store_true", help="Skip Drive sync")
    run_parser.add_argument("--download", action="store_true", help="Download output logs onto local")

    args = parser.parse_args()

    if args.command == "auth":
        install_kaggle_json(args.file)
    elif args.command == "run":
        run_coggle(args)
    elif args.command == "drive-auth":
        authenticate_drive()
    elif args.command == "download-drive":
        download_artifacts_from_drive(args.folder_name, args.target)
    else:
        parser.print_help()

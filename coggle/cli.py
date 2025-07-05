import argparse
from pathlib import Path
from coggle.core.injector import inject_logger
from coggle.core.kaggle_runner import push_kernel, download_outputs, build_kernel_metadata
import os

def run_coggle(args):
    entry_path = Path(args.entry)
    project_dir = entry_path.parent

    if not entry_path.exists():
        print(f"[coggle] Error: Entry file does not exist: {entry_path}")
        return

    # 1. Inject logger
    inject_logger(str(entry_path))

    # 2. Write kernel metadata
    username = os.getenv("KAGGLE_USERNAME", "yourusername")  # Replace with dynamic load later
    slug = project_dir.name.replace(" ", "-").lower()
    metadata = build_kernel_metadata(username, slug, entry_path.name, args.title, private=True, gpu=args.gpu)

    metadata_path = project_dir / "kernel-metadata.json"
    metadata.save(str(metadata_path))

    # 3. Push to Kaggle
    push_kernel(str(project_dir))

    # 4. Download output (optional)
    if args.download:
        download_outputs(f"{username}/{slug}", args.output)

def main():
    parser = argparse.ArgumentParser(prog="coggle", description="Run and manage Kaggle notebook workflows")

    subparsers = parser.add_subparsers(dest="command")

    # coggle run
    run_parser = subparsers.add_parser("run", help="Run and push code to Kaggle")
    run_parser.add_argument("--entry", type=str, required=True, help="Path to your main entry file (e.g. input/main.py)")
    run_parser.add_argument("--output", type=str, default="output", help="Output directory for results/logs")
    run_parser.add_argument("--artifacts", type=str, default="artifacts", help="Artifacts folder to sync to Drive")
    run_parser.add_argument("--gpu", action="store_true", help="Enable GPU on Kaggle")
    run_parser.add_argument("--title", type=str, help="Title of the Kaggle kernel")
    run_parser.add_argument("--drive-folder", type=str, default="coggle-artifacts", help="Google Drive folder to upload to")
    run_parser.add_argument("--no-sync", action="store_true", help="Skip Drive sync")

    args = parser.parse_args()

    if args.command == "run":
        run_coggle(args)
    else:
        parser.print_help()

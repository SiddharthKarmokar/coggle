import os
import shutil
import json
from pathlib import Path

def install_kaggle_json(json_path: str):
    dest_dir = Path.home() / ".kaggle"
    dest_file = dest_dir / "kaggle.json"

    # Validate
    try:
        with open(json_path, "r") as f:
            data = json.load(f)
        if not all(k in data for k in ("username", "key")):
            print("[Error] Invalid kaggle.json: Missing 'username' or 'key'")
            return
    except Exception as e:
        print(f"[Error] Failed to read or parse kaggle.json: {e}")
        return

    # Create .kaggle/ if needed
    os.makedirs(dest_dir, exist_ok=True)

    # Copy file
    shutil.copyfile(json_path, dest_file)

    # Set permissions (optional)
    try:
        os.chmod(dest_file, 0o600)  # Secure permissions on UNIX
    except Exception:
        pass  # Ignore on Windows

    print(f"[Info] kaggle.json successfully installed to {dest_file}")

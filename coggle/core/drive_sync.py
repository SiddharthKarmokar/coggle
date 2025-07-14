import subprocess
import os
import json
from coggle.core import CREDENTIALS_FILE, CONFIG_DIR, CONFIG_PATH, TOKEN_FILE
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

def load_drive_folder_id():
    if not os.path.exists(CONFIG_PATH):
        print("[Warning] Config file not found for Google Drive.")
        return None

    try:
        with open(CONFIG_PATH, "r") as f:
            config = json.load(f)
            return config.get("drive_folder_id")
    except Exception as e:
        print(f"[Error] Failed to read config: {e}")
        return None

def upload_folder_to_drive(local_folder: str, drive_folder_name: str):
    drive = authenticate_drive()

    folder_list = drive.ListFile({
        'q': f"title='{drive_folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
    }).GetList()

    if folder_list:
        parent_id = folder_list[0]['id']
    else:
        folder_metadata = {
            'title': drive_folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        parent = drive.CreateFile(folder_metadata)
        parent.Upload()
        parent_id = parent['id']
        print(f"[Info] Created Drive folder: {drive_folder_name} (ID: {parent_id})")

    for root, _, files in os.walk(local_folder):
        for file in files:
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, local_folder)

            file_metadata = {
                'title': rel_path,
                'parents': [{'id': parent_id}]
            }

            gfile = drive.CreateFile(file_metadata)
            gfile.SetContentFile(full_path)
            gfile.Upload()
            print(f"[Info] Uploaded {rel_path} to Google Drive.")

def sync_artifacts_to_drive(drive_folder_name="coggle-artifacts"):
    artifacts_path = os.path.abspath("artifacts")
    if os.path.isdir(artifacts_path):
        upload_folder_to_drive(artifacts_path, drive_folder_name)
    else:
        print("[Info] No artifacts directory to upload.")

def authenticate_drive():
    """Authenticate with Google Drive and return a PyDrive2 GoogleDrive instance."""

    if not CREDENTIALS_FILE.exists():
        raise FileNotFoundError(f"[Error] credentials.json not found at {CREDENTIALS_FILE}")

    os.makedirs(CONFIG_DIR, exist_ok=True)

    gauth = GoogleAuth()
    gauth.settings['client_config_file'] = str(CREDENTIALS_FILE)
    gauth.LoadCredentialsFile(str(TOKEN_FILE))

    if gauth.credentials is None:
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        gauth.Refresh()
    else:
        gauth.Authorize()

    gauth.SaveCredentialsFile(str(TOKEN_FILE))
    return GoogleDrive(gauth)

def download_artifacts_from_drive(folder_name: str = "coggle-artifacts", local_dir: str = "artifacts"):
    drive = authenticate_drive()

    folder_list = drive.ListFile({
        'q': f"title='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
    }).GetList()

    if not folder_list:
        print(f"[Warning] No folder named '{folder_name}' found on Drive.")
        return

    folder_id = folder_list[0]['id']

    os.makedirs(local_dir, exist_ok=True)

    file_list = drive.ListFile({
        'q': f"'{folder_id}' in parents and trashed=false"
    }).GetList()

    if not file_list:
        print(f"[Info] No files found in '{folder_name}' on Drive.")
        return

    print(f"[Info] Downloading {len(file_list)} files from '{folder_name}'...")

    for file in file_list:
        file_path = os.path.join(local_dir, file['title'])
        print(f"[Info] Downloading: {file['title']} → {file_path}")
        f = drive.CreateFile({'id': file['id']})
        f.GetContentFile(file_path)

    print(f"[Info] All files downloaded to '{local_dir}' successfully.")

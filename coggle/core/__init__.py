from pathlib import Path
import os

CONFIG_DIR = Path.home() / ".coggle"
CREDENTIALS_FILE = CONFIG_DIR / "credentials.json"
TOKEN_FILE = CONFIG_DIR / "token.json"
CONFIG_PATH = os.path.expanduser("~/.coggle_config.json")

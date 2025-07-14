# Coggle — Run & Sync Kaggle Code with Google Drive

Coggle is a Python CLI tool that allows you to:

- Push local Python scripts to Kaggle Notebooks and run them with optional GPU
- Automatically download results and logs from Kaggle
- Sync artifacts to and from Google Drive (as NAS-style storage)
- Authenticate with both Kaggle and Google Drive via CLI

---

## Features

- Push and execute Python scripts on Kaggle
- GPU toggle support
- Output and log auto-download
- Google Drive sync using PyDrive2
- Simple CLI-based authentication for Kaggle and Drive

---

## Installation

```bash
git clone https://github.com/yourusername/coggle.git
cd coggle
pip install -e .
````

---

## CLI Commands

### Authenticate with Kaggle

```bash
coggle auth --file path/to/kaggle.json
```

Sets up Kaggle CLI credentials.

---

### Authenticate with Google Drive

```bash
coggle drive-auth
```

Authenticates using your `credentials.json` file (you’ll be prompted to log in and authorize).

---

### Run a Python script on Kaggle

```bash
coggle run \
  --entry input/main.py \
  --title "Example Kernel" \
  --output output \
  --artifacts artifacts \
  --drive-folder coggle-artifacts \
  --gpu \
  --download
```

**Options:**

* `--entry`: Main script file path (e.g., `input/main.py`)
* `--title`: Title of the Kaggle kernel
* `--output`: Directory to store Kaggle outputs
* `--artifacts`: Directory for Drive-syncable artifacts
* `--gpu`: Enable GPU in Kaggle kernel
* `--download`: Download Kaggle outputs after execution
* `--drive-folder`: Remote Drive folder name
* `--no-sync`: Skip Google Drive sync

---

### Download from Google Drive

```bash
coggle download-drive --folder-name coggle-artifacts --target local_folder/
```

Downloads all files from a named Google Drive folder to the specified local directory.

---

## Example Workflow

1. Authenticate with Kaggle:

```bash
coggle auth --file ~/.kaggle/kaggle.json
```

2. Authenticate with Google Drive:

```bash
coggle drive-auth
```

3. Prepare your script in `input/main.py`

4. Run and sync:

```bash
coggle run --entry input/main.py --gpu --download
```

5. Later, download your artifacts:

```bash
coggle download-drive --folder-name coggle-artifacts --target artifacts/
```

---

## Project Structure

```
coggle/
  core/         # Core logic (auth, kernel, drive)
  config/       # Environment or runtime settings
  schemas/      # Kernel metadata schema
  utils/        # Helpers and reusable code
  exceptions/   # Custom exceptions

input/          # Your source scripts
output/         # Downloaded logs and results
artifacts/      # Files for Google Drive sync
```

---

## Requirements

* Python 3.8+
* [Kaggle API](https://github.com/Kaggle/kaggle-api) (`pip install kaggle`)
* [PyDrive2](https://github.com/iterative/PyDrive2) (`pip install PyDrive2`)
* Google OAuth `credentials.json` for Drive login

---
import subprocess
import os
from pathlib import Path
from subprocess import run, CalledProcessError
from coggle.schemas.kernel_metadata import KernelMetadata
from coggle.exceptions import KaggleAuthError

def build_kernel_metadata(username: str, slug: str, code_file: str, title: str, private=True, gpu=False):
    return KernelMetadata(
        id=f"{username}/{slug}",
        title=title or slug.replace("-", " ").title(),
        code_file=Path(code_file).name,
        is_private=private,
        enable_gpu=gpu
    )

def push_kernel(project_path: str):
    try:
        result = run(
            ["kaggle", "kernels", "push", "-p", project_path],
            check=True,
            capture_output=True,
            text=True
        )
        print("[Info] Kernel pushed to Kaggle.")
    except CalledProcessError as e:
        stderr = e.stderr or ""
        if "Could not find kaggle.json" in stderr:
            raise KaggleAuthError()
        print("[Error] Failed to push kernel.")
        print(stderr.strip())
        raise e

def download_outputs(kernel_id: str, out_dir: str):
    os.makedirs(out_dir, exist_ok=True)
    try:
        subprocess.run(["kaggle", "kernels", "output", kernel_id, "-p", out_dir], check=True)
        print(f"[coggle] Outputs downloaded to {out_dir}")
    except subprocess.CalledProcessError:
        print("[coggle] Warning: No outputs found or kernel hasn’t finished yet.")

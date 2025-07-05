import subprocess
import os
from pathlib import Path
from coggle.schemas.kernel_metadata import KernelMetadata

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
        subprocess.run(["kaggle", "kernels", "push", "-p", project_path], check=True)
        print("[coggle] Kernel pushed to Kaggle.")
    except subprocess.CalledProcessError as e:
        print("[coggle] Error: Failed to push kernel.")
        raise e

def download_outputs(kernel_id: str, out_dir: str):
    os.makedirs(out_dir, exist_ok=True)
    try:
        subprocess.run(["kaggle", "kernels", "output", kernel_id, "-p", out_dir], check=True)
        print(f"[coggle] Outputs downloaded to {out_dir}")
    except subprocess.CalledProcessError:
        print("[coggle] Warning: No outputs found or kernel hasn’t finished yet.")

import os

TEE_IDENTIFIER = "# === COGGLE_TEE_LOGGING ==="

TEE_CODE = f"""
{TEE_IDENTIFIER}
import sys
import os

os.makedirs("logs", exist_ok=True)

class Tee:
    def __init__(self, filename):
        self.file = open(filename, "w")
        self.stdout = sys.stdout
        self.stderr = sys.stderr
        sys.stdout = self
        sys.stderr = self

    def write(self, data):
        self.file.write(data)
        self.stdout.write(data)
        self.file.flush()

    def flush(self):
        self.file.flush()
        self.stdout.flush()

Tee("logs/output.log")
"""

def inject_logger(filepath: str) -> bool:
    """
    Injects logging code into the specified Python file.

    Args:
        filepath (str): Path to the Python script.

    Returns:
        bool: True if injection happened, False if already injected.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        contents = f.read()

    if TEE_IDENTIFIER in contents:
        print(f"[coggle] Logging already injected in {filepath}")
        return False

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(TEE_CODE.strip() + "\n\n" + contents)

    print(f"[coggle] Injected logging code into {filepath}")
    return True

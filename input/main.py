# === COGGLE_TEE_LOGGING ===
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

print('Hello world')
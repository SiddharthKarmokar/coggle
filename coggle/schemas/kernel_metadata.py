from pydantic import BaseModel
from typing import Optional

class KernelMetadata(BaseModel):
    id: str
    title: str
    code_file: str
    language: str = "python"
    kernel_type: str = "script"
    is_private: bool = True
    enable_gpu: bool = False
    enable_internet: bool = True
    dataset_sources: Optional[list[str]] = []
    competition_sources: Optional[list[str]] = []
    kernel_sources: Optional[list[str]] = []

    def save(self, path: str):
        import json
        with open(path, "w") as f:
            json.dump(self.dict(), f, indent=2)

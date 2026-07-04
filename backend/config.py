"""Backend configuration dataclass placeholder."""
from dataclasses import dataclass

@dataclass
class Config:
    index_path: str = "data/index.db"
    docs_path: str = "raw/"
    model_name: str = "local-model-placeholder"

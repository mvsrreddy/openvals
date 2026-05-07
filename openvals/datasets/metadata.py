import json
from pathlib import Path

BASE_DIR = Path(__file__).parent


def load_dataset_metadata(domain):
    path = BASE_DIR / domain / "dataset.json"

    if not path.exists():
        raise FileNotFoundError(
            f"Metadata not found: {path}"
        )

    with open(path, "r") as f:
        return json.load(f)
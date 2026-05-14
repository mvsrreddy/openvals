import json
from pathlib import Path

BASE_DIR = Path(__file__).parent


def load_builtin_dataset(domain, level="advanced"):
    """
    Load built-in OpenVals datasets.

    Example:
        load_builtin_dataset("finance")
        load_builtin_dataset("healthcare")
    """

    dataset_path = BASE_DIR / domain / f"{level}.json"

    if not dataset_path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {dataset_path}"
        )

    with open(dataset_path, "r") as f:
        return json.load(f)
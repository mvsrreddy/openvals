from openvals.datasets.loader import load_builtin_dataset
from openvals.datasets.metadata import load_dataset_metadata

# Load dataset
dataset = load_builtin_dataset("finance")

# Load metadata
meta = load_dataset_metadata("finance")

print("\n=== DATASET ===")
print(dataset[:2])

print("\n=== METADATA ===")
print(meta)
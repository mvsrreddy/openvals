from pathlib import Path
import yaml


BASE_DIR = Path(__file__).resolve().parent


def load_config(config_name: str):

    config_path = BASE_DIR / "presets" / f"{config_name}.yaml"

    if not config_path.exists():
        raise FileNotFoundError(
            f"Config not found: {config_path}"
        )

    with open(config_path, "r") as f:
        return yaml.safe_load(f)
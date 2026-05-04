import configparser
import tomllib
from pathlib import Path

from figroot.constants import CONFIG_DIR
from figroot.utils import get_nested

ALLOWED_EXT = frozenset((".toml", ".yaml", ".yml", ".ini", ".cfg"))


def load_toml(file_path):
    with open(file_path, "rb") as f:
        return tomllib.load(f)


def load_yaml(file_path):
    try:
        import yaml
    except ImportError:
        raise RuntimeError("yaml config is not supported")
    with open(file_path, "r") as f:
        return yaml.safe_load(f) or {}


def load_ini(file_path):
    config = configparser.ConfigParser()
    config.read(file_path)
    return {s: dict(config.items(s)) for s in config.sections()}


def _parse_file(path: Path) -> dict:
    if path.suffix == ".toml":
        return load_toml(path)
    if path.suffix in (".yaml", ".yml"):
        return load_yaml(path)
    return load_ini(path)


def load_configs(tool: str) -> dict:
    root, name = Path.cwd(), tool.lower()

    # Priority: CONFIG_DIR > root (stops at first match)
    for d in [root / CONFIG_DIR, root]:
        if not d.exists():
            continue
        for f in d.glob(f"*{name}.*"):
            if f.is_file() and f.suffix.lower() in ALLOWED_EXT:
                return _parse_file(f)

    pyproject = root / "pyproject.toml"
    if pyproject.exists():
        toml_data = load_toml(pyproject)
        return get_nested(toml_data, f"tool.{tool}")
    return {}

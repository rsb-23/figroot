import os
from pathlib import Path


def _parse_dotenv(path: str | None) -> dict:
    if not path or not Path(path).exists():
        return {}
    res = {}
    for line in open(path):
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            res[k.strip()] = v.strip().strip("\"'")
    return res


def load_envs(tool: str, env_file: str = None) -> dict:
    pfx = f"{tool.upper()}_"
    # Priority: os.env < .env < env_file
    merged = {}
    for src in [dict(os.environ), _parse_dotenv(".env"), _parse_dotenv(env_file)]:
        for k, v in src.items():
            if not k.startswith(pfx):
                continue
            nested = k[len(pfx) :].replace("__", ".").lower()
            cur = merged
            parts = nested.split(".")
            for part in parts[:-1]:
                cur = cur.setdefault(part, {})
            cur[parts[-1]] = v
    return merged

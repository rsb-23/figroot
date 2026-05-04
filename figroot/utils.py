import copy


def deep_merge(base: dict, override: dict) -> dict:
    for k, v in override.items():
        if not v:
            continue
        v = copy.deepcopy(v)
        if k in base and isinstance(base[k], dict) and isinstance(v, dict):
            deep_merge(base[k], v)
        else:
            base[k] = v
    return base


def get_nested(data: dict, key: str, default=None):
    val = data
    for k in key.split("."):
        val = val.get(k) if isinstance(val, dict) else None
        if val is None:
            return default
    return val

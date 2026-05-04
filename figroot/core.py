from figroot.env_loader import load_envs
from figroot.file_loader import load_configs
from figroot.utils import deep_merge, get_nested


class _Node:
    def __init__(self, data: dict):
        self._data = data

    def __getattr__(self, name):
        if name in self._data:
            value = self._data[name]
            if isinstance(value, dict):
                return _Node(value)
            return value
        raise AttributeError(f"Missing attribute: {name}")

    def get(self, key: str, default=None):
        return get_nested(self._data, key, default)

    def __getitem__(self, k):
        return self.get(k)

    def __repr__(self):
        return repr(self._data)


class Config(_Node):
    def __init__(self, tool: str, env_file: str = "", config_file_name: str = ""):

        assert "." not in config_file_name, "file name must not contain '.'"

        # Load raw sources
        self.from_file = _Node(load_configs(config_file_name or tool))
        self.from_env = _Node(load_envs(tool, env_file))

        # Merge with priority: file < env
        merged = {}
        deep_merge(merged, self.from_file._data)
        deep_merge(merged, self.from_env._data)

        super().__init__(merged)

    def __repr__(self):
        return str(self._data)

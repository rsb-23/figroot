# FigRoot

|                |                                                                                             |
|----------------|---------------------------------------------------------------------------------------------|
| Compatibility  | ![Py-Version]                                                                               |
| Quality Checks | [![lint check][lint-badge]]() [![tests][tests-badge]]() [![pre-commit][pre-commit-badge]]() |
| Package        | ![pypi-v] ![pypi-downloads]                                                                 |
| MetaData       | [![license-badge]][license]                                                                 |                                                                                                                                                                                           

Lightweight, modular configuration handler for CLI tools. Supports strict priority merging, dot-notation access, and
multi-format parsing.

## ✨ Features

- **Strict Priority**: `env_file` > `.env` > `os.env` > `config_file`
- **Fast Discovery**: Single-pass `glob` lookup across supported formats
- **Dot Notation**: `cfg.server.port` or `cfg.get("server.port")`
- **Source Isolation**: Access raw data via `cfg.from_env` & `cfg.from_file`
- **Modular**: Use loaders independently or combined
- **Python 3.8+**: Zero core deps (`tomli` auto-fallback for <3.11)

## 📦 Installation

```bash
pip install figroot          # Core (TOML, INI, CFG)
pip install figroot[yaml]    # + YAML support
```

## 🚀 Quick Start

```python
from figroot import Config

cfg = Config("mytool", env_file=".env.local")

# Dot / bracket / fallback access
print(cfg.server.port)  # "8080"
print(cfg.get("db.host", "localhost"))
print(cfg["cache.ttl"])

# Isolate sources (unmerged)
print(cfg.from_env.db.host)  # Env vars only
print(cfg.from_file.db.host)  # Config files only
```

## 🔍 Resolution Priority

### Environment Variables

| Source               | Priority   |
|----------------------|------------|
| `env_file` parameter | 🥇 Highest |
| Project `.env`       | 🥈         |
| `os.environ`         | 🥉 Lowest  |

### Config Files

| Location                           | Priority             |
|------------------------------------|----------------------|
| `_config_/` folder                 | 🥇 Highest           |
| Project root                       | 🥈                   |
| `pyproject.toml` (`[tool.<name>]`) | 🥉 Merged if present |

## 📖 Env Variable Mapping

Prefix: `<TOOL>_` (uppercase) | Nesting: `__` → `.`

```bash
export MYTOOL_SERVER__PORT=8080
export MYTOOL_DATABASE__HOST=pg.local
```

↓

```python
cfg.server.port  # "8080"
cfg.database.host  # "pg.local"
```

## 🛠️ API Reference

### `Config(tool: str, env_file: str | None = None)`

- `.from_file` / `.from_env`: Raw source data (`_Node`)
- `.get(key: str, default=None)`: Dot-string access with fallback
- `__getattr__` / `__getitem__`: Direct dot/bracket access

### Standalone Loaders

```python
from figroot import load_envs, load_configs

env_data = load_envs("mytool", env_file=".env")
file_data = load_configs("mytool")
```

## 🧪 Testing

```bash
pip install pytest pyyaml tomli
pytest tests/ -v --tb=short
```

[license]: https://github.com/rsb-23/figroot/blob/main/LICENSE

[lint-badge]: https://github.com/rsb-23/figroot/actions/workflows/code-lint.yml/badge.svg

[tests-badge]: https://github.com/rsb-23/figroot/actions/workflows/code-test.yml/badge.svg

[license-badge]: https://img.shields.io/badge/License-MIT-blue.svg

[pre-commit-badge]: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white

[py-version]: https://img.shields.io/pypi/pyversions/figroot

[pypi-downloads]: https://img.shields.io/pypi/dm/figroot?label=Downloads

[pypi-v]: https://img.shields.io/pypi/v/figroot?label=latest

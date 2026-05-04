import pytest

from figroot import load_configs
from figroot.constants import CONFIG_DIR


def test_config_discovery_priority(tmp_tool_root):
    cfg_dir = tmp_tool_root / CONFIG_DIR
    cfg_dir.mkdir()
    # CONFIG_DIR wins over root
    (tmp_tool_root / "abc.toml").write_text("x = 1")
    (cfg_dir / "abc.toml").write_text("y = 2")

    data = load_configs("abc")
    assert "y" in data  # Picked from CONFIG_DIR
    assert "x" not in data


def test_pyproject_fallback(tmp_tool_root):
    (tmp_tool_root / "pyproject.toml").write_text('[tool.abc]\nversion = "1.0"\n')
    assert load_configs("abc")["version"] == "1.0"


def test_yaml_config_loading(tmp_tool_root):
    pytest.importorskip("yaml")  # Auto-skips if pyyaml missing

    cfg_dir = tmp_tool_root / CONFIG_DIR
    cfg_dir.mkdir()

    (cfg_dir / "abc.yaml").write_text("""
server:
  port: 9090
  host: "0.0.0.0"
debug: true
""")

    data = load_configs("abc")
    assert data["server"]["port"] == 9090
    assert data["server"]["host"] == "0.0.0.0"
    assert data["debug"] is True

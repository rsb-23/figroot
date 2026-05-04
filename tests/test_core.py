import pytest

from figroot import Config


def test_dot_notation_and_priority(tmp_tool_root, monkeypatch):
    (tmp_tool_root / "abc.toml").write_text("server = { port = 80, timeout = 30 }")
    monkeypatch.setenv("ABC_SERVER__PORT", "8080")

    cfg = Config("abc")

    # Env overrides file
    assert cfg.server.port == "8080"
    # File-only key preserved
    assert cfg.server.timeout == 30

    # Raw sources unchanged
    assert cfg.from_file.server.port == 80
    assert cfg.from_env.server.port == "8080"

    # Fallback & bracket access
    assert cfg.get("missing.key", "fallback") == "fallback"
    assert cfg["server.timeout"] == 30


def test_missing_attribute_error(tmp_tool_root):
    (tmp_tool_root / "abc.toml").write_text("db = { host = 'localhost' }")
    cfg = Config("abc")

    with pytest.raises(AttributeError, match="Missing attribute: server"):
        _ = cfg.server.port

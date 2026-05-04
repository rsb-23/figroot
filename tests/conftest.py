import pytest


@pytest.fixture
def tmp_tool_root(tmp_path, monkeypatch):
    """Isolate cwd and return a temp project root"""
    monkeypatch.chdir(tmp_path)
    return tmp_path

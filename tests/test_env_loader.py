from figroot import load_envs


def test_env_parsing_and_prefix(monkeypatch):
    monkeypatch.setenv("ABC_DB__HOST", "pg_host")
    monkeypatch.setenv("ABC_DB__PORT", "5432")
    monkeypatch.setenv("OTHER_TOKEN", "skip")

    data = load_envs("abc")
    assert data["db"]["host"] == "pg_host"
    assert data["db"]["port"] == "5432"
    assert "other_token" not in data


def test_env_file_priority(tmp_tool_root, monkeypatch):
    # .env
    (tmp_tool_root / ".env").write_text("ABC_KEY=env_dot")
    # Custom env file
    custom = tmp_tool_root / ".custom"
    custom.write_text("ABC_KEY=custom_file")

    # Priority: os.env < .env < env_file
    monkeypatch.setenv("ABC_KEY", "os_env")
    assert load_envs("abc", env_file=str(custom))["key"] == "custom_file"

import pytest
from pydantic import ValidationError

from core.config.settings import Settings


def test_production_requires_jwt_secret(monkeypatch):
    monkeypatch.delenv("JWT_SECRET", raising=False)
    with pytest.raises(ValidationError):
        Settings(app_env="production", _env_file=None)


def test_production_rejects_short_secret():
    with pytest.raises(ValidationError):
        Settings(app_env="production", jwt_secret="short", _env_file=None)


def test_development_generates_random_secret(monkeypatch):
    monkeypatch.delenv("JWT_SECRET", raising=False)
    with pytest.warns(UserWarning):
        s = Settings(app_env="development", _env_file=None)
    assert s.jwt_secret and len(s.jwt_secret) >= 32


def test_empty_env_values_are_ignored(monkeypatch):
    monkeypatch.setenv("DISCORD_GUILD_ID", "")
    assert Settings(_env_file=None).discord_guild_id is None

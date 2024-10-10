import os
import pytest
from src.core.config import Settings

@pytest.fixture
def env_vars():
    os.environ["DATABASE_URL"] = "postgresql://user:pass@localhost/testdb"
    os.environ["SECRET_KEY"] = "testsecretkey"
    os.environ["ALGORITHM"] = "HS256"
    yield
    del os.environ["DATABASE_URL"]
    del os.environ["SECRET_KEY"]
    del os.environ["ALGORITHM"]

def test_settings_from_env(env_vars):
    settings = Settings()
    assert settings.database_url == "postgresql://user:pass@localhost/testdb"
    assert settings.secret_key == "testsecretkey"
    assert settings.algorithm == "HS256"

def test_settings_default_values():
    settings = Settings()
    assert settings.access_token_expire_minutes == 30
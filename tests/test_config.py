import pytest
from unittest.mock import patch
from bot.config import load


@pytest.fixture(autouse=True)
def no_dotenv():
    with patch("bot.config.load_dotenv"):
        yield


def test_load_returns_all_fields(monkeypatch):
    monkeypatch.setenv("TICKET_URL", "https://example.com")
    monkeypatch.setenv("BUYER_NAME", "Test User")
    monkeypatch.setenv("BUYER_EMAIL", "test@example.com")
    monkeypatch.setenv("BUYER_PASSWORD", "secret")
    config = load()
    assert config["url"] == "https://example.com"
    assert config["name"] == "Test User"
    assert config["email"] == "test@example.com"
    assert config["password"] == "secret"


def test_load_exits_when_url_missing(monkeypatch):
    monkeypatch.delenv("TICKET_URL", raising=False)
    monkeypatch.setenv("BUYER_NAME", "Test User")
    monkeypatch.setenv("BUYER_EMAIL", "test@example.com")
    monkeypatch.setenv("BUYER_PASSWORD", "secret")
    with pytest.raises(SystemExit):
        load()


def test_load_exits_when_name_missing(monkeypatch):
    monkeypatch.setenv("TICKET_URL", "https://example.com")
    monkeypatch.delenv("BUYER_NAME", raising=False)
    monkeypatch.setenv("BUYER_EMAIL", "test@example.com")
    monkeypatch.setenv("BUYER_PASSWORD", "secret")
    with pytest.raises(SystemExit):
        load()


def test_load_exits_when_email_missing(monkeypatch):
    monkeypatch.setenv("TICKET_URL", "https://example.com")
    monkeypatch.setenv("BUYER_NAME", "Test User")
    monkeypatch.delenv("BUYER_EMAIL", raising=False)
    monkeypatch.setenv("BUYER_PASSWORD", "secret")
    with pytest.raises(SystemExit):
        load()


def test_load_exits_when_password_missing(monkeypatch):
    monkeypatch.setenv("TICKET_URL", "https://example.com")
    monkeypatch.setenv("BUYER_NAME", "Test User")
    monkeypatch.setenv("BUYER_EMAIL", "test@example.com")
    monkeypatch.delenv("BUYER_PASSWORD", raising=False)
    with pytest.raises(SystemExit):
        load()

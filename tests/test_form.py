from unittest.mock import MagicMock, patch
from bot.form import fill


def _make_config():
    return {
        "url": "https://example.com",
        "name": "Test User",
        "email": "test@example.com",
        "password": "1234",
    }


def test_fill_navigates_to_url():
    config = _make_config()
    mock_element = MagicMock()
    with patch("bot.form.WebDriverWait") as mock_wait:
        mock_wait.return_value.until.return_value = mock_element
        driver = MagicMock()
        fill(driver, config)
    driver.get.assert_called_once_with("https://example.com")


def test_fill_clears_and_sends_keys_for_each_field():
    config = _make_config()
    mock_element = MagicMock()
    with patch("bot.form.WebDriverWait") as mock_wait:
        mock_wait.return_value.until.return_value = mock_element
        driver = MagicMock()
        fill(driver, config)
    assert mock_element.clear.call_count == 3
    mock_element.send_keys.assert_any_call("Test User")
    mock_element.send_keys.assert_any_call("test@example.com")
    mock_element.send_keys.assert_any_call("1234")

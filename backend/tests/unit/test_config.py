"""Unit tests for application configuration."""

from app.config import DevSettings, TestSettings, get_settings


class TestDevSettings:
    """Tests for DevSettings."""

    def test_dev_settings_defaults(self, monkeypatch):
        """DevSettings has development ENV and correct DATABASE_URL."""
        monkeypatch.delenv("ENV", raising=False)
        settings = DevSettings()
        assert settings.ENV == "development"
        assert "youtube_todo" in settings.DATABASE_URL
        assert "youtube_todo_test" not in settings.DATABASE_URL


class TestTestSettings:
    """Tests for TestSettings."""

    def test_test_settings_defaults(self):
        """TestSettings has test ENV and correct DATABASE_URL."""
        settings = TestSettings()
        assert settings.ENV == "test"
        assert "youtube_todo_test" in settings.DATABASE_URL


class TestGetSettings:
    """Tests for get_settings function."""

    def test_get_settings_default(self, monkeypatch):
        """get_settings returns DevSettings when ENV is not set."""
        monkeypatch.delenv("ENV", raising=False)
        result = get_settings()
        assert isinstance(result, DevSettings)

    def test_get_settings_test(self, monkeypatch):
        """get_settings returns TestSettings when ENV=test."""
        monkeypatch.setenv("ENV", "test")
        result = get_settings()
        assert isinstance(result, TestSettings)

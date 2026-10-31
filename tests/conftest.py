import pytest


@pytest.fixture(autouse=True)
def plain_by_default(monkeypatch):
    """Colour off unless a test asks for it, whatever the surrounding environment says."""
    monkeypatch.delenv("FORCE_COLOR", raising=False)
    monkeypatch.delenv("NO_COLOR", raising=False)


@pytest.fixture
def coloured(monkeypatch):
    """Colour on, as if stdout were a terminal."""
    monkeypatch.setenv("FORCE_COLOR", "1")

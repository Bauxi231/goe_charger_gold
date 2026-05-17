"""Fixtures for goe_charger_gold tests."""

import pytest

# Enable custom integrations for testing
pytest_plugins = "pytest_homeassistant_custom_component"


@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(enable_custom_integrations):
    """Enable custom integrations."""
    yield

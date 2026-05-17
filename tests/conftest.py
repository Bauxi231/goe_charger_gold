"""Fixtures for goe_charger_gold tests."""

import pytest

# Activate the custom component plugin
pytest_plugins = "pytest_homeassistant_custom_component"


@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(enable_custom_integrations):
    """Enable custom integrations for all tests."""
    yield

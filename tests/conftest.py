"""Fixtures for goe_charger_gold tests."""

import sys
from pathlib import Path

import pytest

# Add the parent directory to sys.path so we can import the integration
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(enable_custom_integrations):
    """Enable custom integrations."""
    yield

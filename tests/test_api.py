"""Tests for the goe_charger_gold API."""

import pytest


async def test_api_import():
    """Test that the API module can be imported."""
    # This test just checks that the module exists and can be imported
    # We don't need to instantiate it for this basic test
    try:
        from goe_charger_gold import api

        assert api is not None
    except ImportError:
        pytest.fail("Could not import goe_charger_gold.api")

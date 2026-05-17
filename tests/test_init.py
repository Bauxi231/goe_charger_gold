"""Tests for the goe_charger_gold integration."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

import goe_charger_gold
from goe_charger_gold import async_setup_entry
from goe_charger_gold.const import DOMAIN


@pytest.fixture
def mock_config_entry():
    """Mock a config entry."""
    entry = MagicMock()
    entry.data = {"host": "192.168.1.1", "token": ""}
    entry.title = "go-e Charger"
    entry.runtime_data = None
    return entry


@pytest.fixture
def mock_api():
    """Mock the API."""
    api = MagicMock()
    api.test_connection = AsyncMock(return_value=True)
    api.get_status = AsyncMock(return_value={"fna": "go-e Charger", "fwv": "59.4"})
    api.close = AsyncMock()
    return api


@pytest.fixture
def mock_coordinator():
    """Mock the coordinator."""
    coordinator = MagicMock()
    coordinator.async_config_entry_first_refresh = AsyncMock()
    coordinator.device_info = {"identifiers": {(DOMAIN, "192.168.1.1")}}
    coordinator.data = {"fna": "go-e Charger"}
    coordinator.last_update_success = True
    coordinator.last_exception = None
    return coordinator


async def test_async_setup_entry(hass, mock_config_entry, mock_api, mock_coordinator):
    """Test setting up the integration."""
    with (
        patch("goe_charger_gold.GoeChargerAPI", return_value=mock_api),
        patch(
            "goe_charger_gold.GoeChargerCoordinator",
            return_value=mock_coordinator,
        ),
    ):
        result = await async_setup_entry(hass, mock_config_entry)
        assert result is True
        assert mock_config_entry.runtime_data is not None

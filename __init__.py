"""The goe_charger_gold integration."""

from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_TOKEN
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady

from .api import GoEChargerAPI
from .const import DEFAULT_NAME
from .coordinator import GoEChargerCoordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[str] = ["sensor", "number", "switch", "select"]


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Set up goe_charger_gold from a config entry."""
    host = config_entry.data[CONF_HOST]
    token = config_entry.data.get(CONF_TOKEN)

    api = GoEChargerAPI(hass, host, token)
    coordinator = GoEChargerCoordinator(
        hass, api, host, config_entry.title or DEFAULT_NAME
    )

    try:
        await coordinator.async_config_entry_first_refresh()
    except Exception as err:
        _LOGGER.error("Failed to initialize charger at %s: %s", host, err)
        await api.close()
        raise ConfigEntryNotReady(f"Could not connect to charger: {err}") from err

    config_entry.runtime_data = coordinator
    await hass.config_entries.async_forward_entry_setups(config_entry, PLATFORMS)

    _LOGGER.info("go-e Charger Gold integration setup complete for %s", host)
    return True


async def async_unload_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(
        config_entry, PLATFORMS
    )

    if unload_ok:
        coordinator: GoEChargerCoordinator = config_entry.runtime_data
        await coordinator.api.close()
        config_entry.runtime_data = {}

    _LOGGER.info(
        "go-e Charger Gold integration unloaded for %s",
        config_entry.data[CONF_HOST],
    )
    return unload_ok

"""Diagnostics for the goe_charger_gold integration."""

from __future__ import annotations

from typing import Any

from homeassistant.components.diagnostics import async_redact_data
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_TOKEN
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceEntry

from .coordinator import GoEChargerCoordinator

TO_REDACT = {CONF_TOKEN, "ssid", "key", "bssid", "staticIp", "staticGateway"}


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    coordinator: GoEChargerCoordinator = config_entry.runtime_data

    return {
        "entry": {
            "title": config_entry.title,
            "data": async_redact_data(config_entry.data, TO_REDACT),
            "options": async_redact_data(dict(config_entry.options), TO_REDACT),
        },
        "device": {
            "id": coordinator.device_info.get("identifiers"),
            "name": coordinator.device_info.get("name"),
            "manufacturer": coordinator.device_info.get("manufacturer"),
            "model": coordinator.device_info.get("model"),
            "sw_version": coordinator.device_info.get("sw_version"),
            "serial_number": coordinator.device_info.get("serial_number"),
        },
        "data": coordinator.data,
        "last_update_success": coordinator.last_update_success,
        "last_update_error": (
            str(coordinator.last_exception) if coordinator.last_exception else None
        ),
    }


async def async_get_device_diagnostics(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    device: DeviceEntry,
) -> dict[str, Any]:
    """Return diagnostics for a device entry."""
    coordinator: GoEChargerCoordinator = config_entry.runtime_data

    return {
        "device": {
            "id": device.id,
            "name": device.name_by_user or device.name,
            "manufacturer": device.manufacturer,
            "model": device.model,
        },
        "data": coordinator.data,
        "last_update_success": coordinator.last_update_success,
        "last_update_error": (
            str(coordinator.last_exception) if coordinator.last_exception else None
        ),
    }

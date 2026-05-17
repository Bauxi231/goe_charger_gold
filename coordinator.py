"""Data Update Coordinator for goe_charger_gold."""

import logging
from datetime import timedelta
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import GoEChargerAPI, GoEChargerAPIError
from .const import (
    CAR_CHARGING,
    CAR_COMPLETE,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
    FRC_OFF,
    STATUS_CHARGING,
)

_LOGGER = logging.getLogger(__name__)


class GoEChargerCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Class to manage fetching go-e Charger data."""

    def __init__(
        self,
        hass: HomeAssistant,
        api: GoEChargerAPI,
        host: str,
        name: str,
    ) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=name,
            update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL),
        )
        self.api = api
        self.host = host
        self._device_info = None

    @property
    def device_info(self) -> dict[str, Any]:
        """Return device info for the registry."""
        if self._device_info is None and self.data:
            self._device_info = {
                "identifiers": {(DOMAIN, self.host)},
                "name": self.data.get("fna", "go-e Charger"),
                "manufacturer": "go-e",
                "model": self.data.get("typ", "go-eCharger"),
                "sw_version": self.data.get("fwv"),
                "serial_number": self.data.get("sse"),
                "configuration_url": f"http://{self.host}",
            }
        return self._device_info

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from the go-e Charger API."""
        try:
            status_data = await self.api.get_status()

            # Parse nrg array: [U_L1, U_L2, U_L3, U_N, I_L1, I_L2, I_L3, P_L1, P_L2, P_L3, P_N, P_Total, ...]
            nrg = status_data.get("nrg", [])

            # Extract values safely
            voltage_l1 = nrg[0] if len(nrg) > 0 else 0.0
            voltage_l2 = nrg[1] if len(nrg) > 1 else 0.0
            voltage_l3 = nrg[2] if len(nrg) > 2 else 0.0
            current_l1 = nrg[4] if len(nrg) > 4 else 0.0
            current_l2 = nrg[5] if len(nrg) > 5 else 0.0
            current_l3 = nrg[6] if len(nrg) > 6 else 0.0

            # CRITICAL: Use P_Total from API (index 11) if available, else calculate
            # Index 11 is P_Total according to API docs
            total_power_raw = nrg[11] if len(nrg) > 11 else 0.0

            # If API returns 0 for total but we have currents, calculate fallback
            if total_power_raw == 0 and (current_l1 or current_l2 or current_l3):
                # Fallback calculation if API total is missing/buggy
                total_power_raw = (
                    (voltage_l1 * current_l1)
                    + (voltage_l2 * current_l2)
                    + (voltage_l3 * current_l3)
                )

            # CRITICAL: Ghost Power Fix
            # If frc=1 (OFF) or car not charging, power must be 0
            frc = status_data.get("frc", 0)
            car_state = status_data.get("car", 0)
            sta = status_data.get("sta", 0)

            # Check if actually charging:
            # 1. frc must NOT be OFF (1)
            # 2. car must be CHARGING (2) or COMPLETE (4) (if charging just finished)
            # 3. sta bit 2 (Charging) must be set, OR acu (actual current) is not null
            is_charging = (
                frc != FRC_OFF
                and car_state in [CAR_CHARGING, CAR_COMPLETE]
                and (sta & STATUS_CHARGING or status_data.get("acu") is not None)
            )

            # Apply Ghost Power Fix
            total_power = total_power_raw if is_charging else 0.0

            # Build data dictionary
            data = {
                # Charging State
                "is_charging": is_charging,
                "total_power": total_power,
                "power_l1": voltage_l1 * current_l1,
                "power_l2": voltage_l2 * current_l2,
                "power_l3": voltage_l3 * current_l3,
                "current_l1": current_l1,
                "current_l2": current_l2,
                "current_l3": current_l3,
                "voltage_l1": voltage_l1,
                "voltage_l2": voltage_l2,
                "voltage_l3": voltage_l3,
                # Control Values
                "amp": status_data.get("amp", 0),
                "ama": status_data.get("ama", 16),
                "mca": status_data.get("mca", 6),
                "frc": frc,
                "acs": status_data.get("acs", 0),
                "fup": status_data.get("fup", False),
                "fzf": status_data.get("fzf", False),
                "mod": status_data.get("mod", 0),
                "spl3": status_data.get("spl3", 0),
                # Status
                "sta": sta,
                "car": car_state,
                "err": status_data.get("err", 0),
                "cbl": status_data.get("cbl", 0),
                "acu": status_data.get("acu"),
                # Energy
                "wh": status_data.get("wh", 0),
                "whs": status_data.get("whs", 0),
                "whb": status_data.get("whb", 0),
                "whg": status_data.get("whg", 0),
                "who": status_data.get("who", 0),
                "eto": status_data.get("eto", 0),
                # Hardware Info
                "fwv": status_data.get("fwv", ""),
                "tma": status_data.get("tma", [0, 0]),
                "rssi": status_data.get("rssi", 0),
                "fna": status_data.get("fna", "go-e Charger"),
                "typ": status_data.get("typ", ""),
                "oem": status_data.get("oem", "go-e"),
                "sse": status_data.get("sse", ""),
                # Network
                "ccw_ip": (
                    status_data.get("ccw", {}).get("ip", "")
                    if isinstance(status_data.get("ccw"), dict)
                    else ""
                ),
                # Timestamp
                "utc": status_data.get("utc", ""),
                "loc": status_data.get("loc", ""),
            }

            _LOGGER.debug(
                "Updated data for %s: is_charging=%s, total_power=%.2fW, frc=%s, car=%s, sta=%s",
                self.host,
                is_charging,
                total_power,
                frc,
                car_state,
                sta,
            )

            return data

        except GoEChargerAPIError as err:
            raise UpdateFailed(f"Error communicating with charger: {err}")
        except Exception as err:
            _LOGGER.exception("Unexpected error updating data: %s", err)
            raise UpdateFailed(f"Unexpected error: {err}")

    async def async_set_value(self, field: str, value: Any) -> dict[str, Any]:
        """Set a value on the charger and refresh data."""
        result = await self.api.set_value(field, value)
        await self.async_refresh()
        return result

    async def async_set_multiple_values(self, values: dict[str, Any]) -> dict[str, Any]:
        """Set multiple values on the charger and refresh data."""
        result = await self.api.set_multiple_values(values)
        await self.async_refresh()
        return result

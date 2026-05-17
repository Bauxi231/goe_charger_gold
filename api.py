"""API wrapper for go-e Charger."""

import asyncio
import logging
from typing import Any, Optional

import aiohttp
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError

from .const import API_SET_ENDPOINT, API_STATUS_ENDPOINT, API_TIMEOUT

_LOGGER = logging.getLogger(__name__)


class GoEChargerAPIError(HomeAssistantError):
    """Exception raised for go-e Charger API errors."""

    pass


class GoEChargerAPI:
    """Handle communication with the go-e Charger API."""

    def __init__(
        self, hass: HomeAssistant, host: str, token: Optional[str] = None
    ) -> None:
        """Initialize the API wrapper."""
        self.hass = hass
        self.host = host
        self.token = token
        self._session: Optional[aiohttp.ClientSession] = None

    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create aiohttp session."""
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()
        return self._session

    async def close(self) -> None:
        """Close the aiohttp session."""
        if self._session and not self._session.closed:
            await self._session.close()
            self._session = None

    async def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        """Make HTTP request to the go-e Charger API."""
        session = await self._get_session()
        url = f"http://{self.host}{endpoint}"
        headers = {}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"

        try:
            _LOGGER.debug("Making %s request to %s with params %s", method, url, params)
            async with session.request(
                method, url, headers=headers, params=params, timeout=API_TIMEOUT
            ) as resp:
                resp.raise_for_status()
                return await resp.json()
        except asyncio.TimeoutError:
            _LOGGER.error("Timeout connecting to go-e Charger at %s", self.host)
            raise GoEChargerAPIError(f"Timeout connecting to charger at {self.host}")
        except aiohttp.ClientError as err:
            _LOGGER.error("HTTP error from go-e Charger: %s", err)
            raise GoEChargerAPIError(f"Communication error with charger: {err}")
        except Exception as err:
            _LOGGER.exception("Unexpected error from go-e Charger API: %s", err)
            raise GoEChargerAPIError(f"Unexpected API error: {err}")

    async def get_status(self) -> dict[str, Any]:
        """Get charger status from API."""
        return await self._request("GET", API_STATUS_ENDPOINT)

    async def set_value(self, field: str, value: Any) -> dict[str, Any]:
        """Set a single value on the charger using query parameters."""
        # go-e API v2 expects: /api/set?field=value
        params = {field: value}
        return await self._request("POST", API_SET_ENDPOINT, params)

    async def set_multiple_values(self, values: dict[str, Any]) -> dict[str, Any]:
        """Set multiple values on the charger in one request."""
        # go-e API v2 supports multiple query params: /api/set?field1=val1&field2=val2
        return await self._request("POST", API_SET_ENDPOINT, values)

    async def test_connection(self) -> bool:
        """Test if the charger is reachable."""
        try:
            await self.get_status()
            _LOGGER.info("Successfully connected to go-e Charger at %s", self.host)
            return True
        except GoEChargerAPIError as err:
            _LOGGER.error("Failed to connect to go-e Charger: %s", err)
            return False

"""Switch entities for goe_charger_gold."""

from __future__ import annotations

import logging

from homeassistant.components.switch import (
    SwitchEntity,
    SwitchEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .coordinator import GoEChargerCoordinator

_LOGGER = logging.getLogger(__name__)

SWITCH_ENTITIES: tuple[SwitchEntityDescription, ...] = (
    SwitchEntityDescription(
        key="fup",
        translation_key="force_update",
        icon="mdi:update",
        entity_category=EntityCategory.CONFIG,
    ),
    SwitchEntityDescription(
        key="fzf",
        translation_key="zero_feedin",
        icon="mdi:transmission-tower-off",
        entity_category=EntityCategory.CONFIG,
    ),
    SwitchEntityDescription(
        key="acs",
        translation_key="auth_lock",
        icon="mdi:lock",
        entity_category=EntityCategory.CONFIG,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up switch entities."""
    coordinator: GoEChargerCoordinator = config_entry.runtime_data

    entities: list[GoEChargerSwitch] = []
    for description in SWITCH_ENTITIES:
        entities.append(GoEChargerSwitch(coordinator, description))

    async_add_entities(entities)
    _LOGGER.info("Added %d switch entities", len(entities))


class GoEChargerSwitch(SwitchEntity):
    """Representation of a go-e Charger switch entity."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: GoEChargerCoordinator,
        description: SwitchEntityDescription,
    ) -> None:
        """Initialize the switch entity."""
        self.entity_description = description
        self._attr_unique_id = f"{coordinator.host}_{description.key}"
        self._attr_device_info = coordinator.device_info
        self.coordinator = coordinator

    @property
    def is_on(self) -> bool | None:
        """Return true if the switch is on."""
        if self.coordinator.data is None:
            return None
        value = self.coordinator.data.get(self.entity_description.key)
        if isinstance(value, bool):
            return value
        if isinstance(value, int):
            return value == 1
        return False

    async def async_turn_on(self, **kwargs) -> None:
        """Turn the switch on."""
        field = self.entity_description.key
        _LOGGER.debug("Turning on %s", field)
        await self.coordinator.async_set_value(field, True)

    async def async_turn_off(self, **kwargs) -> None:
        """Turn the switch off."""
        field = self.entity_description.key
        _LOGGER.debug("Turning off %s", field)
        await self.coordinator.async_set_value(field, False)

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self.coordinator.data is not None

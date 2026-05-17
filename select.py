"""Select entities for goe_charger_gold."""

from __future__ import annotations

import logging

from homeassistant.components.select import (
    SelectEntity,
    SelectEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .coordinator import GoEChargerCoordinator

_LOGGER = logging.getLogger(__name__)

SELECT_ENTITIES: tuple[SelectEntityDescription, ...] = (
    SelectEntityDescription(
        key="frc",
        translation_key="force_control",
        icon="mdi:power-standby",
        options=["0", "1", "2"],
        entity_category=EntityCategory.CONFIG,
    ),
    SelectEntityDescription(
        key="mod",
        translation_key="charging_mode",
        icon="mdi:ev-plug-type2",
        options=[str(i) for i in range(64)],
        entity_category=EntityCategory.CONFIG,
    ),
    SelectEntityDescription(
        key="spl3",
        translation_key="phase_switch",
        icon="mdi:sine-wave",
        options=["0", "1"],
        entity_category=EntityCategory.CONFIG,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up select entities."""
    coordinator: GoEChargerCoordinator = config_entry.runtime_data

    entities: list[GoEChargerSelect] = []
    for description in SELECT_ENTITIES:
        entities.append(GoEChargerSelect(coordinator, description))

    async_add_entities(entities)
    _LOGGER.info("Added %d select entities", len(entities))


class GoEChargerSelect(SelectEntity):
    """Representation of a go-e Charger select entity."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: GoEChargerCoordinator,
        description: SelectEntityDescription,
    ) -> None:
        """Initialize the select entity."""
        self.entity_description = description
        self._attr_unique_id = f"{coordinator.host}_{description.key}"
        self._attr_device_info = coordinator.device_info
        self.coordinator = coordinator

    @property
    def current_option(self) -> str | None:
        """Return the current option."""
        if self.coordinator.data is None:
            return None
        value = self.coordinator.data.get(self.entity_description.key)
        if value is not None:
            return str(value)
        return None

    async def async_select_option(self, option: str) -> None:
        """Select a new option."""
        field = self.entity_description.key
        _LOGGER.debug("Selecting %s for %s", option, field)
        await self.coordinator.async_set_value(field, option)

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self.coordinator.data is not None

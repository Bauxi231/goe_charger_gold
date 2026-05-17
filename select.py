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

# DEFINITION: Nur frc
SELECT_ENTITIES: tuple[SelectEntityDescription, ...] = (
    SelectEntityDescription(
        key="frc",
        translation_key="force_control",
        icon="mdi:power-standby",
        options=["0", "1", "2"],
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

    _LOGGER.critical("=== SETUP SELECT ENTITIES CALLED ===")
    _LOGGER.critical("Coordinator host: %s", coordinator.host)
    _LOGGER.critical("Coordinator data available: %s", coordinator.data is not None)
    if coordinator.data:
        _LOGGER.critical("Data keys: %s", list(coordinator.data.keys()))
        _LOGGER.critical("'frc' in data: %s", "frc" in coordinator.data)
        _LOGGER.critical("frc value: %s", coordinator.data.get("frc"))

    entities: list[GoEChargerSelect] = []
    for description in SELECT_ENTITIES:
        _LOGGER.critical("Processing entity: %s", description.key)
        try:
            entity = GoEChargerSelect(coordinator, description)
            entities.append(entity)
            _LOGGER.critical("Created entity: %s", entity.unique_id)
        except Exception as e:
            _LOGGER.exception("Failed to create entity %s: %s", description.key, e)

    _LOGGER.critical("Adding %d entities", len(entities))
    async_add_entities(entities)
    _LOGGER.critical("=== SETUP SELECT ENTITIES FINISHED ===")


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
        _LOGGER.critical("Initializing entity: %s", self._attr_unique_id)

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

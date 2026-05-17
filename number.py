"""Number entities for goe_charger_gold."""

from __future__ import annotations

import logging

from homeassistant.components.number import (
    NumberEntity,
    NumberEntityDescription,
    NumberMode,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfElectricCurrent
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import MAX_AMPERE, MIN_AMPERE
from .coordinator import GoEChargerCoordinator

_LOGGER = logging.getLogger(__name__)

NUMBER_ENTITIES: tuple[NumberEntityDescription, ...] = (
    NumberEntityDescription(
        key="amp",
        translation_key="charging_current",
        native_min_value=MIN_AMPERE,
        native_max_value=MAX_AMPERE,
        native_step=1,
        mode=NumberMode.SLIDER,
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        icon="mdi:current-ac",
    ),
    NumberEntityDescription(
        key="ama",
        translation_key="max_current_limit",
        native_min_value=MIN_AMPERE,
        native_max_value=32,
        native_step=1,
        mode=NumberMode.SLIDER,
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        icon="mdi:current-ac",
        entity_category=EntityCategory.CONFIG,
    ),
    NumberEntityDescription(
        key="mca",
        translation_key="min_current_limit",
        native_min_value=6,
        native_max_value=MAX_AMPERE,
        native_step=1,
        mode=NumberMode.SLIDER,
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        icon="mdi:current-ac",
        entity_category=EntityCategory.CONFIG,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up number entities."""
    coordinator: GoEChargerCoordinator = config_entry.runtime_data

    entities: list[GoEChargerNumber] = []
    for description in NUMBER_ENTITIES:
        entities.append(GoEChargerNumber(coordinator, description))

    async_add_entities(entities)
    _LOGGER.info("Added %d number entities", len(entities))


class GoEChargerNumber(NumberEntity):
    """Representation of a go-e Charger number entity."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: GoEChargerCoordinator,
        description: NumberEntityDescription,
    ) -> None:
        """Initialize the number entity."""
        self.entity_description = description
        self._attr_unique_id = f"{coordinator.host}_{description.key}"
        self._attr_device_info = coordinator.device_info
        self.coordinator = coordinator

    @property
    def native_value(self) -> float | None:
        """Return the current value."""
        if self.coordinator.data is None:
            return None
        value = self.coordinator.data.get(self.entity_description.key)
        if value is not None:
            return float(value)
        return None

    async def async_set_native_value(self, value: float) -> None:
        """Set a new value."""
        field = self.entity_description.key
        int_value = int(value)
        _LOGGER.debug("Setting %s to %d", field, int_value)
        await self.coordinator.async_set_value(field, int_value)

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self.coordinator.data is not None

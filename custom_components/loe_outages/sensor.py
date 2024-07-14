"""Calendar platform for Loe outages integration."""

import logging
from collections.abc import Callable
from dataclasses import dataclass

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import STATE_OFF, STATE_ON
from .coordinator import LoeOutagesCoordinator
from .entity import LoeOutagesEntity

LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True, kw_only=True)
class LoeOutagesSensorDescription(SensorEntityDescription):
    """Loe Outages entity description."""

    val_func: Callable[[LoeOutagesCoordinator], bool]


def get_next_outage(coordinator: LoeOutagesCoordinator) -> str:
    """Return the next outage."""
    event = coordinator.get_next_event(STATE_OFF)
    LOGGER.debug("Events: %s", event)


SENSOR_TYPES: tuple[LoeOutagesSensorDescription, ...] = (
    LoeOutagesSensorDescription(
        key="electricity",
        translation_key="electricity",
        icon="mdi:transmission-tower",
        device_class=SensorDeviceClass.ENUM,
        options=[STATE_ON, STATE_OFF],
        val_func=lambda coordinator: coordinator.current_state,
    ),
    LoeOutagesSensorDescription(
        key="next_outage",
        translation_key="next_outage",
        icon="mdi:calendar-remove",
        device_class=SensorDeviceClass.TIMESTAMP,
        val_func=lambda coordinator: coordinator.next_outage,
    ),
    LoeOutagesSensorDescription(
        key="next_connectivity",
        translation_key="next_connectivity",
        icon="mdi:calendar-check",
        device_class=SensorDeviceClass.TIMESTAMP,
        val_func=lambda coordinator: coordinator.next_connectivity,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Loe outages calendar platform."""
    LOGGER.debug("Setup new entry: %s", config_entry)
    coordinator: LoeOutagesCoordinator = config_entry.runtime_data
    async_add_entities(
        LoeOutagesSensor(coordinator, description) for description in SENSOR_TYPES
    )


class LoeOutagesSensor(LoeOutagesEntity, SensorEntity):
    """Implementation of connection entity."""

    def __init__(
        self,
        coordinator: LoeOutagesCoordinator,
        entity_description: LoeOutagesSensorDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.entity_description = entity_description
        self._attr_unique_id = (
            f"{coordinator.config_entry.entry_id}-"
            f"{coordinator.group}-"
            f"{self.entity_description.key}"
        )

    @property
    def native_value(self) -> str | None:
        """Return the state of the sensor."""
        return self.entity_description.val_func(self.coordinator)
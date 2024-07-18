"""Calendar platform for Loe outages integration."""

import datetime
import logging
import pytz

from homeassistant.components.calendar import CalendarEntity, CalendarEvent
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityDescription
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .coordinator import LoeOutagesCoordinator
from .entity import LoeOutagesEntity

LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Loe outages calendar platform."""
    LOGGER.debug("Setup new entry: %s", config_entry)
    coordinator: LoeOutagesCoordinator = config_entry.runtime_data
    async_add_entities([LoeOutagesCalendar(coordinator)])


class LoeOutagesCalendar(LoeOutagesEntity, CalendarEntity):
    """Implementation of calendar entity."""

    def __init__(
        self,
        coordinator: LoeOutagesCoordinator,
    ) -> None:
        """Initialize the LoeOutagesCalendar entity."""
        super().__init__(coordinator)
        self.entity_description = EntityDescription(
            key="calendar",
            name="Calendar",
            translation_key="calendar",
        )
        self._attr_unique_id = (
            f"{coordinator.config_entry.entry_id}-"
            f"{coordinator.group}-"
            f"{self.entity_description.key}"
        )

    @property
    def event(self) -> CalendarEvent | None:
        """Return the current or next upcoming event or None."""
        utc = pytz.UTC
        now = datetime.datetime.now().astimezone(utc)
        LOGGER.debug("Getting current event for %s", now)
        res = self.coordinator.get_calendar_at(now)
        return res

    async def async_get_events(
        self,
        hass: HomeAssistant,  # noqa: ARG002
        start_date: datetime.datetime,
        end_date: datetime.datetime,
    ) -> list[CalendarEvent]:
        """Return calendar events within a datetime range."""
        LOGGER.debug('Getting all events between "%s" -> "%s"', start_date, end_date)
        return self.coordinator.get_calendar_between(start_date, end_date)

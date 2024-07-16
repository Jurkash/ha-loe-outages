"""Coordinator for Loe outages integration."""

import datetime
import logging

from .models import Interval
from homeassistant.components.calendar import CalendarEvent
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.translation import async_get_translations
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.util import dt as dt_utils

from .api import LoeOutagesApi
from .const import (
    CONF_GROUP,
    DOMAIN,
    STATE_OFF,
    STATE_ON,
    TRANSLATION_KEY_EVENT_OFF,
    TRANSLATION_KEY_EVENT_ON,
    UPDATE_INTERVAL,
)

LOGGER = logging.getLogger(__name__)

TIMEFRAME_TO_CHECK = datetime.timedelta(hours=24)


class LoeOutagesCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Loe outages data."""

    config_entry: ConfigEntry

    def __init__(self, hass: HomeAssistant, config_entry: ConfigEntry) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            LOGGER,
            name=DOMAIN,
            update_interval=datetime.timedelta(seconds=UPDATE_INTERVAL),
        )
        self.hass = hass
        self.config_entry = config_entry
        self.translations = {}
        self.group = config_entry.options.get(
            CONF_GROUP,
            config_entry.data.get(CONF_GROUP),
        )
        self.api = LoeOutagesApi(self.group)

    @property
    def event_name_map(self) -> dict:
        """Return a mapping of event names to translations."""
        return {
            STATE_OFF: self.translations.get(TRANSLATION_KEY_EVENT_OFF),
            STATE_ON: self.translations.get(TRANSLATION_KEY_EVENT_ON),
        }

    async def update_config(
        self,
        hass: HomeAssistant,  # noqa: ARG002
        config_entry: ConfigEntry,
    ) -> None:
        """Update configuration."""
        new_group = config_entry.options.get(CONF_GROUP)
        if new_group and new_group != self.group:
            LOGGER.debug("Updating group from %s -> %s", self.group, new_group)
            self.group = new_group
            self.api = LoeOutagesApi(self.group)
            await self.async_refresh()
        else:
            LOGGER.debug("No group update necessary.")

    async def _async_update_data(self) -> None:
        """Fetch data from API."""
        try:
            await self.async_fetch_translations()
            return await self.api.async_fetch_schedule()
        except FileNotFoundError as err:
            LOGGER.exception("Cannot read file for group %s", self.group)
            msg = f"File not found: {err}"
            raise UpdateFailed(msg) from err

    async def async_fetch_translations(self) -> None:
        """Fetch translations."""
        LOGGER.debug("Fetching translations for %s", DOMAIN)
        self.translations = await async_get_translations(
            self.hass,
            self.hass.config.language,
            "common",
            [DOMAIN],
        )
        LOGGER.debug("Translations loaded: %s", self.translations)

    def _get_next_event_of_type(self, state_type: str) -> Interval | None:
        """Get the next event of a specific type."""
        now = dt_utils.now()
        # Sort events to handle multi-day spanning events correctly
        next_events = sorted(
            self.get_events_between(
                now,
                now + TIMEFRAME_TO_CHECK,
                translate=False,
            ),
            key=lambda event: event.startTime,
        )
        LOGGER.debug("Next events: %s", next_events)
        for event in next_events:
            if self._event_to_state(event) == state_type and event.startTime > now:
                return event
        return None

    @property
    def next_outage(self) -> datetime.datetime | None:
        """Get the next outage time."""
        event = self._get_next_event_of_type(STATE_OFF)
        LOGGER.debug("Next outage: %s", event)
        return event.startTime if event else None

    @property
    def next_connectivity(self) -> datetime.datetime | None:
        """Get next connectivity time."""
        now = dt_utils.now()
        current_event = self.get_event_at(now)
        # If current event is OFF, return the end time
        if self._event_to_state(current_event) == STATE_OFF:
            return current_event.endTime

        # Otherwise, return the next on event's end
        event = self._get_next_event_of_type(STATE_ON)
        LOGGER.debug("Next connectivity: %s", event)
        return event.startTime if event else None

    @property
    def current_state(self) -> str:
        """Get the current state."""
        now = dt_utils.now()
        event = self.get_event_at(now)
        return self._event_to_state(event)

    def get_event_at(self, at: datetime.datetime) -> Interval:
        """Get the current event."""
        event = self.api.get_current_event(at)
        return self._get_interval_event(event, translate=False)

    def get_events_between(
        self,
        start_date: datetime.datetime,
        end_date: datetime.datetime,
        *,
        translate: bool = True,
    ) -> list[Interval]:
        """Get all events."""
        events = self.api.get_events(start_date, end_date)
        return [
            self._get_interval_event(event, translate=translate) for event in events
        ]

    def get_calendar_at(self, at: datetime.datetime) -> CalendarEvent:
        """Get the current event."""
        event = self.api.get_current_event(at)
        return self._get_calendar_event(event, translate=False)

    def get_calendar_between(
        self,
        start_date: datetime.datetime,
        end_date: datetime.datetime,
        *,
        translate: bool = True,
    ) -> list[CalendarEvent]:
        """Get all events."""
        events = self.api.get_events(start_date, end_date)
        return [
            self._get_calendar_event(event, translate=translate) for event in events
        ]

    def _get_interval_event(
        self,
        event: dict | None,
        *,
        translate: bool = True,
    ) -> Interval:
        """Transform an event into a Inteval."""
        if not event:
            return None

        event_summary = event["state"]
        translated_summary = self.event_name_map.get(event_summary)
        event_start = event["startTime"]
        event_end = event["endTime"]

        LOGGER.debug(
            "Transforming event: %s (%s -> %s)",
            event_summary,
            event_start,
            event_end,
        )

        return Interval(
            state=translated_summary if translate else event_summary,
            startTime=event_start,
            endTime=event_end,
        )

    def _get_calendar_event(
        self,
        event: dict | None,
        *,
        translate: bool = True,
    ) -> CalendarEvent:
        """Transform an event into a Inteval."""
        if not event:
            return None

        event_summary = event["state"]
        translated_summary = self.event_name_map.get(event_summary)
        event_start = dt_utils.as_local(event["startTime"])
        event_end = dt_utils.as_local(event["endTime"])

        LOGGER.debug(
            "Transforming event: %s (%s -> %s)",
            event_summary,
            event_start,
            event_end,
        )

        return CalendarEvent(
            summary=translated_summary if translate else event_summary,
            start=event_start,
            end=event_end,
            description=event_summary,
        )

    def _event_to_state(self, event: Interval | None) -> str:
        state = event.state if event else None
        return {
            STATE_ON: STATE_ON,
            STATE_OFF: STATE_OFF,
            None: STATE_ON,
        }[state]

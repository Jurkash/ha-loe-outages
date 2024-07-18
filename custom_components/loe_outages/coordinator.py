"""Coordinator for Loe outages integration."""

import datetime
import logging
import pytz

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

    async def async_update_config(
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
            return await self.api.async_fetch_schedules()
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
        now = dt_utils.now().astimezone(pytz.UTC)
        # Sort events to handle multi-day spanning events correctly
        next_events = sorted(
            self.get_intervals_between(
                now,
                (now + TIMEFRAME_TO_CHECK).astimezone(pytz.UTC),
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
        event = self._get_next_event_of_type(STATE_ON)
        LOGGER.debug("Next connectivity: %s", event)
        return event.startTime if event else None

    @property
    def current_state(self) -> str:
        """Get the current state."""
        now = dt_utils.now().astimezone(pytz.UTC)
        event = self.get_interval_at(now)
        return self._event_to_state(event)

    def get_interval_at(self, at: datetime.datetime) -> Interval | None:
        """Get the current event."""
        event = self.api.get_current_event(at)
        return self._get_interval_event(event, translate=False)

    def get_intervals_between(
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

    def _get_interval_event(
        self,
        interval: Interval | None,
        *,
        translate: bool = True,
    ) -> Interval:
        """Transform an event into a Inteval."""
        if not interval:
            return None

        interval_summary = interval.state
        translated_summary = self.event_name_map.get(interval_summary)

        LOGGER.debug(
            "Transforming event: %s (%s -> %s)",
            interval_summary,
            interval.startTime,
            interval.endTime,
        )

        return Interval(
            state=translated_summary if translate else interval_summary,
            startTime=interval.startTime,
            endTime=interval.endTime,
        )

    def get_calendar_at(self, at: datetime.datetime) -> CalendarEvent | None:
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

    def _get_calendar_event(
        self,
        interval: Interval | None,
        *,
        translate: bool = True,
    ) -> CalendarEvent:
        """Transform an event into a Inteval."""
        if not interval:
            return None

        interval_summary = interval.state
        translated_summary = self.event_name_map.get(interval_summary)

        LOGGER.debug(
            "Transforming event: %s (%s -> %s)",
            interval_summary,
            interval.startTime,
            interval.endTime,
        )

        return CalendarEvent(
            summary=translated_summary if translate else interval_summary,
            start=interval.startTime,
            end=interval.endTime,
            description=interval_summary,
        )

    def _event_to_state(self, event: Interval | None) -> str:
        state = event.state if event else None
        return {
            STATE_ON: STATE_ON,
            STATE_OFF: STATE_OFF,
            None: STATE_ON,
        }[state]

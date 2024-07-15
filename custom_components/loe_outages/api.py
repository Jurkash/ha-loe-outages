"""API for Loe outages."""

import logging
import aiohttp
from .models import OutageSchedule
import datetime
import pytz

LOGGER = logging.getLogger(__name__)


class LoeOutagesApi:
    """Class to interact with API for Loe outages."""

    schedule: list[OutageSchedule]

    def __init__(self, group: str) -> None:
        """Initialize the LoeOutagesApi."""
        self.group = group
        self.schedule = []

    async def async_fetch_latest_json(self) -> dict:
        """Fetch outages from the async API endpoint."""
        url = "https://lps.yuriishunkin.com/api/Schedule/latest"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data
                else:
                    LOGGER.error(f"Failed to fetch schedule: {response.status}")
                    return None

    async def async_fetch_all_json(self) -> dict:
        """Fetch outages from the async API endpoint."""
        url = "https://lps.yuriishunkin.com/api/Schedule/all"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data
                else:
                    LOGGER.error(f"Failed to fetch schedule: {response.status}")
                    return None

    async def async_fetch_schedule(self) -> None:
        """Fetch outages from the JSON response."""
        if len(self.schedule) == 0:
            schedule_data = await self.async_fetch_all_json()
            schedules = OutageSchedule.from_list(schedule_data)
            for schedule in sorted(schedules, key=lambda s: s.date):
                self.schedule.append(schedule)
            return
        else:
            schedule_data = await self.async_fetch_latest_json()
            schedule = OutageSchedule.from_dict(schedule_data)

            new_schedule = OutageSchedule.from_dict(schedule_data)
            self.schedule = [
                item
                for item in self.schedule
                if item.dateString != new_schedule.dateString
            ]
            self.schedule.append(new_schedule)
            self.schedule.sort(key=lambda item: item.dateString)

        self.schedule = sorted(self.schedule, key=lambda s: s.date)

    def get_current_event(self, at: datetime) -> dict:
        """Get the current event."""
        if not self.schedule:
            return None

        twoDaysBefore = datetime.datetime.now() + datetime.timedelta(days=-2)
        for schedule in reversed(self.schedule):
            if schedule.date < twoDaysBefore.astimezone(pytz.UTC):
                return None

            events_at = schedule.get_current_event(self.group, at)
            if not events_at:
                return None
            return events_at  # return only the first event

    def get_events(
        self,
        start_date: datetime.datetime,
        end_date: datetime.datetime,
    ) -> list[dict]:
        """Get all events."""
        if not self.schedule:
            return []

        result = []
        twoDaysBeforeStart = start_date + datetime.timedelta(days=-2)
        for schedule in reversed(self.schedule):
            if schedule.date < twoDaysBeforeStart:
                break

            for interval in schedule.between(self.group, start_date, end_date):
                result.append(interval)

        return result

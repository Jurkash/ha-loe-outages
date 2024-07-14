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

    async def async_fetch_json_from_endpoint(self) -> dict:
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

    async def async_fetch_schedule(self) -> None:
        """Fetch outages from the JSON response."""
        schedule_data = await self.async_fetch_json_from_endpoint()
        schedule = OutageSchedule.from_dict(schedule_data)
        if len(self.schedule) == 0:
            self.schedule.append(schedule)
            return

        if self.schedule[-1].id != schedule.id:
            if self.schedule[-1].dateString == schedule.dateString:
                self.schedule.remove(self.schedule[-1])
            self.schedule.append(schedule)

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

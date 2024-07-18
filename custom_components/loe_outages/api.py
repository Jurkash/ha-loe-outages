"""API for Loe outages."""

import logging
import aiohttp
import datetime
import pytz
from .models import OutageSchedule, Interval

LOGGER = logging.getLogger(__name__)


class LoeOutagesApi:
    """Class to interact with API for Loe outages."""

    schedules: list[OutageSchedule]

    def __init__(self, group: str) -> None:
        """Initialize the LoeOutagesApi."""
        self.group = group
        self.schedules = []

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

    async def async_fetch_schedules(self) -> None:
        """Fetch outages from the JSON response."""
        if len(self.schedules) == 0:
            LOGGER.debug("Fetching all schedules")
            schedules_data = await self.async_fetch_all_json()
            schedules = OutageSchedule.from_list(schedules_data)
            for schedule in sorted(schedules, key=lambda s: s.date):
                self.schedules.append(schedule)
            return None
        else:
            LOGGER.debug("Fetching latest schedules")
            schedule_data = await self.async_fetch_latest_json()
            new_schedule = OutageSchedule.from_dict(schedule_data)
            self.schedules = [
                item
                for item in self.schedules
                if item.dateString != new_schedule.dateString
            ]
            self.schedules.append(new_schedule)
        self.schedules.sort(key=lambda item: item.date)
        LOGGER.debug("Saved schedules %s", list(map(lambda s: s.date, self.schedules)))
        return None

    def get_current_event(self, at: datetime.datetime) -> Interval | None:
        """Get the current event."""
        if not self.schedules or len(self.schedules) == 0:
            LOGGER.debug("No schedules found")
            return None

        at = at.astimezone(pytz.UTC)
        twoDaysBefore = (at + datetime.timedelta(days=-2)).astimezone(pytz.UTC)
        for schedule in reversed(self.schedules):
            LOGGER.debug("Schedule to compare: %s < %s", schedule.date, twoDaysBefore)
            if schedule.date < twoDaysBefore:
                return None

            events_at = schedule.get_current_event(self.group, at)
            if events_at is not None:
                LOGGER.debug("Some event was found: %s", events_at)
                return events_at  # return only the first event

        LOGGER.debug("No evets at found")
        return None

    def get_events(
        self,
        start_date: datetime.datetime,
        end_date: datetime.datetime,
    ) -> list[Interval]:
        """Get all events."""
        if not self.schedules or len(self.schedules) == 0:
            return []

        start_date = start_date.astimezone(pytz.UTC)
        end_date = end_date.astimezone(pytz.UTC)
        result = []
        twoDaysBeforeStart = (start_date + datetime.timedelta(days=-2)).astimezone(
            pytz.UTC
        )
        for schedule in reversed(self.schedules):
            if schedule.date < twoDaysBeforeStart:
                break

            for interval in schedule.intersect(self.group, start_date, end_date):
                result.append(interval)

        return self._merge_intervals(sorted(result, key=lambda i: i.startTime))

    def _merge_intervals(self, intervals: list[Interval]) -> list[Interval]:
        if not intervals:
            return []

        # Start with the first interval
        merged_intervals = [intervals[0]]

        for current in intervals[1:]:
            last = merged_intervals[-1]
            if last.endTime == current.startTime and last.state == current.state:
                merged_intervals[-1] = Interval(
                    startTime=last.startTime, endTime=current.endTime, state=last.state
                )
            else:
                merged_intervals.append(current)
        [
            LOGGER.debug("merged: from: %s, to: %s", inter.startTime, inter.endTime)
            for inter in merged_intervals
        ]
        return merged_intervals

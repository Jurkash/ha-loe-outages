"""API for LOE outages."""

import datetime
import logging
import requests

from .const import API_BASE_URL

LOGGER = logging.getLogger(__name__)


class LoeOutagesApi:
    """Class to interact with the API for LOE outages."""

    def __init__(self, group: str) -> None:
        """Initialize the LOE OutagesApi."""
        self.group = group
        self.api_base_url = API_BASE_URL

    def fetch_schedule(self) -> list[dict]:
        """Fetch outages from the API."""
        url = f"{self.api_base_url}/Schedule/latest"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        for group in data["groups"]:
            if group["id"] == self.group:
                return group["intervals"]
        return []

    def get_current_event(self, at: datetime.datetime) -> dict:
        """Get the current event."""
        schedule = self.fetch_schedule()
        current_event = None
        for event in schedule:
            start = datetime.datetime.fromisoformat(event["startTime"])
            end = datetime.datetime.fromisoformat(event["endTime"])
            if start <= at <= end:
                current_event = event
                break
        return current_event

    def get_events(
        self,
        start_date: datetime.datetime,
        end_date: datetime.datetime,
    ) -> list[dict]:
        """Get all events between start_date and end_date."""
        schedule = self.fetch_schedule()
        events = []
        for event in schedule:
            start = datetime.datetime.fromisoformat(event["startTime"])
            end = datetime.datetime.fromisoformat(event["endTime"])
            if start_date <= start <= end_date or start_date <= end <= end_date:
                events.append(event)
        return events

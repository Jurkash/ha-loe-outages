import datetime
import pytz
import logging

utc = pytz.UTC
LOGGER = logging.getLogger(__name__)


class Interval:
    def __init__(
        self, state: str, startTime: datetime.datetime, endTime: datetime.datetime
    ):
        self.state = state
        self.startTime = startTime
        self.endTime = endTime

    @staticmethod
    def from_dict(obj: dict) -> "Interval":
        return Interval(
            state=obj.get("state").lower(),
            startTime=datetime.datetime.fromisoformat(obj.get("startTime")).astimezone(
                utc
            ),
            endTime=datetime.datetime.fromisoformat(obj.get("endTime")).astimezone(utc),
        )

    def to_dict(self) -> dict:
        return {
            "state": self.state,
            "startTime": self.startTime,
            "endTime": self.endTime,
        }


class Group:
    def __init__(self, id: str, intervals: list[Interval]):
        self.id = id
        self.intervals = intervals

    @staticmethod
    def from_dict(obj: dict) -> "Group":
        intervals = [
            Interval.from_dict(interval) for interval in obj.get("intervals", [])
        ]
        return Group(id=obj.get("id"), intervals=intervals)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "intervals": [interval.to_dict() for interval in self.intervals],
        }


class OutageSchedule:
    def __init__(
        self,
        id: str,
        date: datetime.datetime,
        dateString: str,
        imageUrl: str,
        groups: list[Group],
    ):
        self.id = id
        self.date = date
        self.dateString = dateString
        self.imageUrl = imageUrl
        self.groups = groups

    @staticmethod
    def from_list(obj_list: list[dict]) -> list["OutageSchedule"]:
        return [OutageSchedule.from_dict(item) for item in obj_list]

    @staticmethod
    def from_dict(obj: dict) -> "OutageSchedule":
        groups = [Group.from_dict(group) for group in obj.get("groups", [])]
        return OutageSchedule(
            id=obj.get("id"),
            date=datetime.datetime.fromisoformat(obj.get("date")).astimezone(utc),
            dateString=obj.get("dateString"),
            imageUrl=obj.get("imageUrl"),
            groups=groups,
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "date": self.date,
            "dateString": self.dateString,
            "imageUrl": self.imageUrl,
            "groups": [group.to_dict() for group in self.groups],
        }

    def get_current_event(
        self, group_id: str, at: datetime.datetime
    ) -> Interval | None:
        at = at.astimezone(utc)
        for group in self.groups:
            if group.id == group_id:
                for interval in group.intervals:
                    if interval.startTime <= at and at <= interval.endTime:
                        return interval
        return None

    def intersect(
        self, group_id: str, start: datetime.datetime, end: datetime.datetime
    ) -> list[Interval]:
        start = start.astimezone(utc)
        end = end.astimezone(utc)
        res = []
        for group in self.groups:
            if group.id == group_id:
                for interval in group.intervals:
                    if interval.startTime <= end and start <= interval.endTime:
                        res.append(interval)
        return res

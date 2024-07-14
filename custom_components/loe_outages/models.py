import datetime
import pytz
from dateutil import parser
from typing import List

utc=pytz.UTC

class Interval:
    def __init__(self, state: str, startTime: str, endTime: str):
        self.state = state
        self.startTime = startTime
        self.endTime = endTime

    @staticmethod
    def from_dict(obj: dict) -> 'Interval':
        return Interval(
            state=obj.get("state"),
            startTime=parser.parse(obj.get("startTime")).astimezone(utc),
            endTime=parser.parse(obj.get("endTime")).astimezone(utc),
        )

    def to_dict(self) -> dict:
        return {
            "state": self.state,
            "startTime": self.startTime,
            "endTime": self.endTime
        }

class Group:
    def __init__(self, id: str, intervals: List[Interval]):
        self.id = id
        self.intervals = intervals

    @staticmethod
    def from_dict(obj: dict) -> 'Group':
        intervals = [Interval.from_dict(interval) for interval in obj.get("intervals", [])]
        return Group(
            id=obj.get("id"),
            intervals=intervals
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "intervals": [interval.to_dict() for interval in self.intervals]
        }

class OutageSchedule:
    def __init__(self, id: str, date: str, dateString: str, imageUrl: str, groups: List[Group]):
        self.id = id
        self.date = date
        self.dateString = dateString
        self.imageUrl = imageUrl
        self.groups = groups

    @staticmethod
    def from_dict(obj: dict) -> 'OutageSchedule':
        groups = [Group.from_dict(group) for group in obj.get("groups", [])]
        return OutageSchedule(
            id=obj.get("id"),
            date=parser.parse(obj.get("date")).astimezone(utc),
            dateString=obj.get("dateString"),
            imageUrl=obj.get("imageUrl"),
            groups=groups
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "date": self.date,
            "dateString": self.dateString,
            "imageUrl": self.imageUrl,
            "groups": [group.to_dict() for group in self.groups]
        }
    
    def get_current_event(self, group_id: str, at: datetime.datetime) -> dict:
        at = at.astimezone(utc)
        for group in self.groups:
            if group.id == group_id:
                for interval in group.intervals:
                    if interval.startTime <= at <= interval.endTime:
                        return interval.to_dict()
        return {}
    
    def between(self, group_id: str, start: datetime.datetime, end: datetime.datetime) -> list[dict]:
        start = start.astimezone(utc)
        end = end.astimezone(utc)
        res = []
        for group in self.groups:
            if group.id == group_id:
                for interval in group.intervals:
                    if start <= interval.startTime and interval.endTime <= end:
                        res.append(interval.to_dict())
        return res

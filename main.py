from datetime import datetime, timedelta, timezone
import logging
from typing import Optional, Iterable, Callable, TypeVar

logging.basicConfig(level=logging.DEBUG)

from aw_client import ActivityWatchClient

T = TypeVar("T")


def find(pred: Callable[[T], Optional[T]], seq: Iterable[T]):
    for elem in seq:
        if pred(elem):
            return elem
    return None


class Detector:
    def __init__(self):
        self.client = ActivityWatchClient("status-checker")
        buckets = self.client.get_buckets()
        # print(buckets)
        # TODO: We need a better way to query buckets
        window_bucket = find(lambda bucket: bucket["type"] == "currentwindow" and "testing" not in bucket["id"], buckets.values())
        if window_bucket is None:
            raise Exception("Bucket not found")
        self.window_bucket_id = window_bucket["id"]

    def detect(self, filter_str: str):
        last_events = self.client.get_events(self.window_bucket_id, limit=1)
        if last_events:
            last_event = last_events[0]

            found = find(lambda label: filter_str in label, last_event.labels)
            if found:
                print("{} seems to be active!".format(filter_str))


detector = Detector()
detector.detect("aw-detector")
detector.detect("zsh")
detector.detect("chrome")

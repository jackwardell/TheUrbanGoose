from abc import ABC
from collections import defaultdict


class Event(ABC):
    pass


class Handler(ABC):
    pass


class PageHit(Event):
    pass


class EventSystem:
    """
    event system for execution engine
    how to use:
    """

    def __init__(self):
        self.handlers = defaultdict(list)

    def init_app(self, app):
        pass

    def register_handler(self, event_type, handler):
        self.handlers[event_type.__name__].append(handler)

    def send(self, event):
        for handler in self.handlers[event.__class__.__name__]:
            handler(event)

from collections.abc import Callable

from bebop.events.models import Event

subscribers: list[Callable] = []


def subscribe(handler: Callable) -> None:
    subscribers.append(handler)


def emit(event: Event) -> None:
    for handler in subscribers:
        handler(event)

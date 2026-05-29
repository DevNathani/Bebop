from src.bebop.events.bus import emit, subscribe
from src.bebop.events.models import Event
from src.bebop.ui.rich_cli.renderer import (
    handle_event,
)

subscribe(handle_event)

emit(
    Event(
        event_type="info",
        data={"message": "Hello"},
    )
)

emit(
    Event(
        event_type="success",
        data={"message": "Transfer Complete"},
    )
)

emit(
    Event(
        event_type="warning",
        data={"message": "Retrying"},
    )
)

emit(
    Event(
        event_type="error",
        data={"message": "Connection Lost"},
    )
)

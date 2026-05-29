from rich.console import Console

from bebop.events.models import Event

console = Console()

EVENT_STYLES = {
    "info": {"color": "cyan"},
    "success": {"color": "green"},
    "error": {"color": "red"},
    "warning": {"color": "yellow"},
}


def handle_event(event: Event) -> None:
    style = EVENT_STYLES.get(event.event_type)
    if style is None:
        console.print(f"[white][UNKNOWN EVENT] {event.data['message']}[/white]")
    color = style["color"]
    console.print(f"[{color}]{event.data['message']}[/{color}]")

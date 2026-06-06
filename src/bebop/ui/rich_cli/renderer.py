from rich.console import Console
from rich.progress import BarColumn, Progress, TaskProgressColumn, TextColumn

from bebop.events.models import Event

console = Console()

progress = Progress(
    TextColumn("[bold blue]{task.description}"), BarColumn(), TaskProgressColumn()
)

tasks: dict[str, int] = {}
progress_started = False


EVENT_STYLES = {
    "info": {"color": "cyan"},
    "success": {"color": "green"},
    "error": {"color": "red"},
    "warning": {"color": "yellow"},
    "progress": {"color": "cyan"},
}


def handle_event(event: Event) -> None:
    global progress_started

    style = EVENT_STYLES.get(event.event_type)

    if style is None:
        console.print(f"[white][UNKNOWN EVENT] {event.event_type}[/white]")
        return

    if event.event_type == "progress":
        filename = event.data["filename"]
        current = event.data["current_bytes"]
        total = event.data["total"]

        if not progress_started:
            progress.start()
            progress_started = True

        if filename not in tasks:
            task_id = progress.add_task(
                filename,
                total=total,
            )

            tasks[filename] = task_id

        task_id = tasks[filename]

        progress.update(
            task_id,
            completed=current,
        )

        return

    color = style["color"]
    console.print(f"[{color}]{event.data['message']}[/{color}]")

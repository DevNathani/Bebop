import json
from pathlib import Path

# Directory to store checkpoint files
CHECKPOINT_DIR = Path("checkpoints")
CHECKPOINT_DIR.mkdir(exist_ok=True)


def save_checkpoint(filename: str, offset: int, filesize: int, filehash: str) -> None:
    """
    Save current transfer progress.
    """

    checkpoint_file = CHECKPOINT_DIR / f"{filename}.json"

    data = {"offset": offset, "filesize": filesize, "filehash": filehash}

    with checkpoint_file.open("w") as file:
        json.dump(data, file)


def load_checkpoint(filename: str) -> dict:
    """
    Load saved offset.
    Returns 0 if checkpoint does not exist.
    """

    checkpoint_file = CHECKPOINT_DIR / f"{filename}.json"

    if not checkpoint_file.exists():
        return {}

    with checkpoint_file.open("r") as file:
        data = json.load(file)

    return data


def delete_checkpoint(filename: str) -> None:
    """
    Delete checkpoint after successful transfer.
    """

    checkpoint_file = CHECKPOINT_DIR / f"{filename}.json"

    if checkpoint_file.exists():
        checkpoint_file.unlink()

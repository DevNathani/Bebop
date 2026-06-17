from bebop.config.config import TRANSFER_ACCEPT, TRANSFER_REJECT, TRANSFER_REQUEST
from bebop.core.transfer.protocol import (
    create_message,
    receive_message,
)


# Send Transfer Request
def send_transfer_request(
    connection,
    sender_name: str,
    total_files: int,
    total_size: int,
    file_names: list[str],
) -> None:
    """
    Send transfer request to receiver.

    Format:
    TRANSFER_REQUEST|hostname|file_count|total_size|files
    """
    files = ",".join(file_names)
    message = f"{TRANSFER_REQUEST}|{sender_name}|{total_files}|{total_size}|{files}"
    print(message)
    connection.sendall(create_message(message))


# Recieve Transfer Request
def receive_transfer_request(connection) -> tuple[str, int, int, list[str]]:
    message = receive_message(connection).decode()

    request_type, sender_name, total_files, total_size, files = message.split("|")

    if request_type != TRANSFER_REQUEST:
        raise ValueError("Invalid transfer request")
    file_names = files.split(",")
    return (sender_name, int(total_files), int(total_size), file_names)


# Send Accept Message to send all files
def send_accept(connection) -> None:
    connection.sendall(create_message(TRANSFER_ACCEPT))


# Send Reject Message to sender
def send_reject(connection) -> None:
    connection.sendall(create_message(TRANSFER_REJECT))


def receive_response(connection) -> str:
    return receive_message(connection).decode()

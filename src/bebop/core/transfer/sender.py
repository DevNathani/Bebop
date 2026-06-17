import socket

from bebop.config.config import (
    CHUNK_SIZE,
    PORT,
    TRANSFER_ACCEPT,
    TRANSFER_DIR,
)
from bebop.core.discovery.select_device import select_device
from bebop.core.history.db import init_db
from bebop.core.history.devices import upsert_device
from bebop.core.history.sent_files import save_sent_file
from bebop.core.transfer.protocol import create_message, receive_message
from bebop.core.transfer.request import (
    receive_response,
    send_transfer_request,
)
from bebop.core.utils.hash import calculate_sha256
from bebop.core.utils.logger import logger
from bebop.events.bus import emit, subscribe
from bebop.events.models import Event
from bebop.ui.rich_cli.renderer import handle_event


def main() -> None:
    try:
        init_db()
        subscribe(handle_event)
        # creating a socket
        # ( AF_INET defines IPv4 Addressing and SOCK_STREAM defines the TCP )
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        TARGET_HOSTNAME, TARGET_IP = select_device()

        # Perform the 3 way TCP Handshake
        client_socket.connect((TARGET_IP, PORT))

        emit(
            Event(
                event_type="success",
                data={"message": f"Connected to {TARGET_IP} : {PORT}"},
            )
        )

        logger.info(f"Connected to {TARGET_IP} : {PORT}")

        # Transfer Request Mechanism
        sender_name = socket.gethostname()

        files = []
        for file in TRANSFER_DIR.iterdir():
            if file.is_file():
                files.append(file.name)
        print(files)
        total_files = len(files)

        total_size = sum(
            file.stat().st_size for file in TRANSFER_DIR.iterdir() if file.is_file()
        )

        send_transfer_request(
            client_socket,
            sender_name,
            total_files,
            total_size,
            files,
        )

        response = receive_response(client_socket)

        if response != TRANSFER_ACCEPT:
            emit(
                Event(
                    event_type="warning",
                    data={"message": "Transfer Rejected"},
                )
            )

            return

        emit(
            Event(
                event_type="success",
                data={"message": "Transfer Accepted"},
            )
        )
        upsert_device(
            hostname=TARGET_HOSTNAME,
            ip_address=TARGET_IP,
        )
        # Iterate over all files in TRANSFER_DIR/
        for file_path in TRANSFER_DIR.iterdir():
            if not file_path.is_file():
                continue

            # extracting file details from the file object
            file_name = file_path.name
            file_size = file_path.stat().st_size
            # calculate Hash
            file_hash = calculate_sha256(file_path)

            logger.info(f"[FILE] {file_name}")

            print(f"[FILE] {file_name}")
            print(f"[FILE SIZE] {file_size} bytes")
            print(f"[FILE SIZE] {type(file_size)} bytes")
            print(f"[FILE HASH] {file_hash}")

            # Send file name creating the packet with Length Prefix Framing
            # ( len:payload )
            client_socket.sendall(create_message(file_name))

            # send file size
            client_socket.sendall(create_message(str(file_size)))

            client_socket.sendall(create_message(file_hash))

            offset = int(receive_message(client_socket))

            emit(
                Event(
                    event_type="info",
                    data={"message": f"Resume Offset: {offset}"},
                )
            )

            logger.info(f"[RESUME OFFSET] {offset}")

            # send file data as binary ( No need of Length Prefix Framing for file data
            #  since it is the part of body while name and size is part of header)
            send_bytes = offset
            last_percentage = -1
            with file_path.open("rb") as file:
                file.seek(offset)
                while chunk := file.read(CHUNK_SIZE):
                    client_socket.sendall(chunk)

                    send_bytes += len(chunk)

                    current_percentage = int((send_bytes / file_size) * 100)

                    if current_percentage != last_percentage:
                        emit(
                            Event(
                                event_type="progress",
                                data={
                                    "filename": file_name,
                                    "current_bytes": send_bytes,
                                    "total": file_size,
                                },
                            )
                        )

                        last_percentage = current_percentage

            emit(
                Event(
                    event_type="success",
                    data={"message": "File Transfered"},
                )
            )
            save_sent_file(
                filename=file_name,
                size=file_size,
                receiver_name=TARGET_HOSTNAME,
                receiver_ip=TARGET_IP,
                status="success",
            )
            print(f"[HISTORY SAVED] {file_name}")
            logger.info(f"[SUCCESS] {file_name} transferred")

        # Send END package to mark end of directory
        client_socket.sendall(create_message("END"))
        print("[SUCCESS] All files transferred")

    except FileNotFoundError:
        logger.error("[ERROR] File not Found")
        print("[ERROR] File not Found")
    except ConnectionRefusedError:
        logger.error("[ERROR] Connection Refused")
        print("[ERROR] Connection Refused")
    except ConnectionResetError:
        logger.error("[ERROR] Connection Reset by Reciever")
        print("[ERROR] Connection Reset by Reciever")
    except KeyboardInterrupt:
        logger.error("[STOPPED] ABORTED by User")
        print("\n Aborted by User")
    except Exception as error:
        if "file_name" in locals():
            save_sent_file(
                filename=file_name,
                size=file_size,
                receiver_name=TARGET_HOSTNAME,
                receiver_ip=TARGET_IP,
                status="success",
            )

        emit(Event(event_type="error", data={"message": f"[ERROR] {error}"}))

        logger.error(str(error))

    finally:
        if "client_socket" in locals():
            client_socket.close()
        emit(Event(event_type="info", data={"message": "[Session Closed]"}))
        logger.info("[SESSION CLOSED]")


if __name__ == "__main__":
    main()

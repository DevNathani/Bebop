import socket
import threading
from pathlib import Path

from bebop.config.config import (
    CHECKPOINT_INTERVAL,
    PORT,
    RECIEVED_DIR,
    SERVER_HOST,
)
from bebop.core.discovery.listener import start_listener
from bebop.core.transfer.protocol import create_message, receive_message
from bebop.core.transfer.request import (
    receive_transfer_request,
    send_accept,
    send_reject,
)
from bebop.core.utils.checkpoint import (
    delete_checkpoint,
    load_checkpoint,
    save_checkpoint,
)
from bebop.core.utils.hash import calculate_sha256
from bebop.core.utils.logger import logger
from bebop.events.bus import emit, subscribe
from bebop.events.models import Event
from bebop.ui.rich_cli.renderer import handle_event

RECIEVED_DIR.mkdir(exist_ok=True)


def main() -> None:
    connection = None
    try:
        subscribe(handle_event)
        discovery_thread = threading.Thread(
            target=start_listener,
            daemon=True,
        )

        discovery_thread.start()
        # creating a socket
        # ( AF_INET defines IPv4 Addressing and SOCK_STREAM defines the TCP )
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Binding the PORT and HOST to application
        server_socket.bind((SERVER_HOST, PORT))

        # Accept Connections through this socket
        server_socket.listen(1)
        emit(
            Event(
                event_type="info",
                data={"message": f"[LISTENING] Reciever listening on port {PORT}"},
            )
        )

        # Create a new connection socket after accepting request from sender
        connection, address = server_socket.accept()
        logger.info(f"[CONNECTED] Client connected from {address}")

        emit(
            Event(
                event_type="info",
                data={"message": f"[CONNECTED] Client connected from {address}"},
            )
        )

        (sender_name, total_files, total_size, file_names) = receive_transfer_request(
            connection
        )

        print()
        print("=" * 50)

        print("Incoming Transfer Request")

        print(f"From : {sender_name}")

        print(f"Files: {total_files}")

        print(f"Size : {total_size} bytes")

        print()

        for file_name in file_names:
            print(f"  • {file_name}")

        print("=" * 50)
        print()

        choice = input("Accept Transfer? (y/n): ").strip().lower()

        if choice != "y":
            send_reject(connection)

            print("Transfer Rejected")

            connection.close()

            return

        send_accept(connection)

        print("Transfer Accepted")
        # Recieve Every file
        while True:
            # recieve file name from custom created recieve message application protocol
            filename = receive_message(connection).decode()

            # Stop recieving when END file is recieved
            if filename == "END":
                print("SESSION CLOSED")
                break

            # concatenate filepath
            output_path = RECIEVED_DIR / filename

            # recieve file size from custom created recieve message application protocol
            filesize = int(receive_message(connection).decode())

            # Recieve HAsh for Integrity Check
            expected_hash = receive_message(connection).decode()
            print(f"[FILENAME] {filename}")
            print(f"[FILESIZE] {filesize} bytes")
            print(f"[FILE HASH] {expected_hash}")

            checkpoint = load_checkpoint(filename)
            offset = 0
            if (
                checkpoint
                and filesize == checkpoint["filesize"]
                and expected_hash == checkpoint["filehash"]
            ):
                offset = checkpoint["offset"]
            emit(Event(event_type="info", data={"message": f"[OFFSET] : {offset}"}))
            connection.sendall(create_message(str(offset)))

            # Recieve file data
            received_bytes = offset
            last_checkpoint = offset

            mode = "ab" if offset > 0 else "wb"

            with open(output_path, mode) as file:
                while received_bytes < filesize:
                    remaining = filesize - received_bytes

                    chunk_size = min(1024, remaining)
                    chunk = connection.recv(chunk_size)

                    if not chunk:
                        raise ConnectionError("Connection lost during file transfer")

                    file.write(chunk)

                    received_bytes += len(chunk)

                    if received_bytes - last_checkpoint >= CHECKPOINT_INTERVAL:
                        save_checkpoint(
                            filename, received_bytes, filesize, expected_hash
                        )
                        last_checkpoint = received_bytes

                    progress = (received_bytes / filesize) * 100

                    logger.info(f"[RECEIVING] {filename}")

                    print(f"[{filename}] : {progress:.2f}%", end="\r")
            print()

            # Check file integrity
            calculated_hash = calculate_sha256(Path(output_path))
            print("Checking Integrity")
            if calculated_hash == expected_hash:
                print(f"Deleting {filename} checkpoint")
                delete_checkpoint(filename)
                print("INTEGRITY VALID")
            else:
                print("INTEGRITY FAILED")

            # print("[SUCCESS] File received")
            emit(
                Event(
                    event_type="success",
                    data={"message": f"[SUCCESS] File Recieved {filename}"},
                )
            )
            logger.info(f"[SUCCESS] File Recieved {filename}")

        connection.close()
        server_socket.close()
        logger.info("[SESSION CLOSED]")

    except ConnectionError:
        # print("[ERROR] Connection Lost")
        emit(Event(event_type="error", data={"message": "[ERROR] Connection Lost"}))
        logger.error("[ERROR] Connection Lost")

    except KeyboardInterrupt:
        print("\n[STOPPED] User Interruption")
        logger.error("\n[STOPPED] User Interruption")
    except Exception as error:
        print(f"[ERROR] {error}")
        logger.error(str(error))

    finally:
        if connection:
            connection.close()
        server_socket.close()
        emit(Event(event_type="info", data={"message": "[Session Closed]"}))
        logger.info("[SESSION CLOSED]")


if __name__ == "__main__":
    main()

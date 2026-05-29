import socket
from pathlib import Path

from bebop.config.config import PORT, RECIEVED_DIR, SERVER_HOST
from bebop.core.transfer.protocol import receive_message
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

            # Recieve file data
            received_bytes = 0

            with open(output_path, "wb") as file:
                while received_bytes < filesize:
                    # recieve upto pending bytes or max 1024
                    chunk = connection.recv(min(1024, filesize - received_bytes))

                    if not chunk:
                        raise ConnectionError("Connection lost during file transfer")

                    file.write(chunk)  # Write to file

                    received_bytes += len(chunk)

                    progress = (received_bytes / filesize) * 100
                    logger.info(f"[RECIEVING] {filename}")
                    print(f"[{filename}] : {progress:.2f}%", end="\r")

            print()

            # Check file integrity
            calculated_hash = calculate_sha256(Path(output_path))
            if calculated_hash == expected_hash:
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

import socket
from pathlib import Path

from bebop.core.transfer.protocol import receive_message
from bebop.core.utils.hash import calculate_sha256

# Accept request from all network interfaces ( 0.0.0.0 ) allot port 5000 to port
HOST = "0.0.0.0"
PORT = 5000

# named the recieved file
OUTPUT_FILE = "received_sample.txt"


def main() -> None:
    # creating a socket
    # ( AF_INET defines IPv4 Addressing and SOCK_STREAM defines the TCP )
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Binding the PORT and HOST to application
    server_socket.bind((HOST, PORT))

    # Accept Connections through this socket
    server_socket.listen(1)

    print(f"[LISTENING] Receiver listening on port {PORT}")

    # Create a new connection socket after accepting request from sender
    connection, address = server_socket.accept()

    print(f"[CONNECTED] Client connected from {address}")

    # recieve file name from custom created recieve message application protocol
    filename = receive_message(connection).decode()

    # recieve file size from custom created recieve message application protocol
    filesize = int(receive_message(connection).decode())

    expected_hash = receive_message(connection).decode()
    print(f"[FILENAME] {filename}")
    print(f"[FILESIZE] {filesize} bytes")
    print(f"[FILE HASH] {expected_hash}")

    # Recieve file data
    received_bytes = 0

    with open(OUTPUT_FILE, "wb") as file:
        while received_bytes < filesize:
            # recieve upto pending bytes or max 1024
            chunk = connection.recv(min(1024, filesize - received_bytes))

            if not chunk:
                raise ConnectionError("Connection lost during file transfer")

            file.write(chunk)  # Write to file

            received_bytes += len(chunk)

            print(f"[PROGRESS] {received_bytes}/{filesize}")

    calculated_hash = calculate_sha256(Path(OUTPUT_FILE))
    if calculated_hash == expected_hash:
        print("INTEGRITY VALID")

    print("[SUCCESS] File received")

    connection.close()
    server_socket.close()


if __name__ == "__main__":
    main()

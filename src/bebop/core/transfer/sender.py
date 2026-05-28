import socket
from pathlib import Path

from bebop.core.transfer.protocol import create_message
from bebop.core.utils.hash import calculate_sha256

# Define Host and Port of the reciever
HOST = "127.0.0.1"
PORT = 5000

# File needed to be transferred
TRANSFER_DIR = "transfer"


def main() -> None:
    # creating a socket
    # ( AF_INET defines IPv4 Addressing and SOCK_STREAM defines the TCP )
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Perform the 3 way TCP Handshake
    client_socket.connect((HOST, PORT))

    # convert the pathlib object from the file
    transfer_path = Path(TRANSFER_DIR)

    # Iterate over all files in transfer/
    for file_path in transfer_path.iterdir():
        if not file_path.is_file():
            continue

        # extracting file details from the file object
        file_name = file_path.name
        file_size = file_path.stat().st_size
        # calculate Hash
        file_hash = calculate_sha256(file_path)

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
        # send file data as binary ( No need of Length Prefix Framing for file data
        #  since it is the part of body while name and size is part of header)
        send_bytes = 0
        with file_path.open("rb") as file:
            while chunk := file.read(1024):  # read chunk from file till end
                client_socket.sendall(chunk)
                send_bytes += len(chunk)
                progress = (send_bytes / file_size) * 100
                print(f"[{file_name}] : [{progress:.2f}]%")

        print("[SUCCESS] File transferred")

    # Send END package to mark end of directory
    client_socket.sendall(create_message("END"))
    print("[SUCCESS] All files transferred")

    client_socket.close()


if __name__ == "__main__":
    main()

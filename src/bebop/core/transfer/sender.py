import socket

from bebop.config.config import CHUNK_SIZE, CLIENT_HOST, PORT, TRANSFER_DIR
from bebop.core.transfer.protocol import create_message
from bebop.core.utils.hash import calculate_sha256
from bebop.core.utils.logger import logger


def main() -> None:
    try:
        # creating a socket
        # ( AF_INET defines IPv4 Addressing and SOCK_STREAM defines the TCP )
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Perform the 3 way TCP Handshake
        client_socket.connect((CLIENT_HOST, PORT))

        logger.info(f"Connected to {CLIENT_HOST} : {PORT}")

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
            # send file data as binary ( No need of Length Prefix Framing for file data
            #  since it is the part of body while name and size is part of header)
            send_bytes = 0
            with file_path.open("rb") as file:
                while chunk := file.read(CHUNK_SIZE):  # read chunk from file till end
                    client_socket.sendall(chunk)
                    send_bytes += len(chunk)
                    progress = (send_bytes / file_size) * 100
                    print(f"[{file_name}] : [{progress:.2f}]%")

            print("[SUCCESS] File transferred")
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
        logger.error(str(error))
        print(f"[ERROR] {error}")

    finally:
        client_socket.close()
        logger.info("[SESSION CLOSED]")


if __name__ == "__main__":
    main()

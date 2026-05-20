import socket


# Create Message with Length Prefix Message
def create_message(message: str) -> bytes:
    encoded_message = message.encode()
    header = f"{len(encoded_message)}:".encode()
    return header + encoded_message


# Recieve exactly n bytes of data
def receive_exact(connection: socket.socket, size: int) -> bytes:
    data = b""

    while len(data) < size:
        chunk = connection.recv(size - len(data))

        if not chunk:
            raise ConnectionError("Connection closed unexpectedly")

        data += chunk

    return data


# Custom Recieve Message Helper
def receive_message(connection: socket.socket) -> bytes:
    # extract header ( length of data) from message
    header = b""
    while not header.endswith(b":"):
        chunk = connection.recv(1)

        if not chunk:
            raise ConnectionError("Connection closed while reading header")
        header += chunk
    message_length = int(header[:-1].decode())

    # Recieve later n bytes of data
    return receive_exact(connection, message_length)

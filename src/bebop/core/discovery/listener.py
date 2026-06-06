import socket

from bebop.config.config import DISCOVERY_MESSAGE, DISCOVERY_PORT, DISCOVERY_RESPONSE


def start_listener() -> None:
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Bind socket to all network interfaces
    # "" means: 127.0.0.1, 192.168.x.x, 10.x.x.x, Any interface available
    server.bind(("", DISCOVERY_PORT))

    print(f"[DISCOVERY] Listening on UDP Port {DISCOVERY_PORT}")

    # Keep listening forever
    while True:
        data, address = server.recvfrom(1024)

        # Convert bytes -> string
        message = data.decode()

        print(f"[DISCOVERY REQUEST] {address} -> {message}")

        # Only respond to: BEBOP_DISCOVER
        if message != DISCOVERY_MESSAGE:
            continue

        # Get current machine hostname
        hostname = socket.gethostname()

        # Create discovery response BEBOP_RESPONSE:DESKTOP-ABC123
        response = f"{DISCOVERY_RESPONSE}:{hostname}"

        # Send response back to requester
        server.sendto(response.encode(), address)
        print(f"[DISCOVERY RESPONSE] Sent to {address}")

        print(f"[HOSTNAME] {hostname}")


if __name__ == "__main__":
    start_listener()

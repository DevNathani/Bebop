import socket
from time import time

from bebop.config.config import DISCOVERY_MESSAGE, DISCOVERY_PORT, DISCOVERY_RESPONSE


def discover_devices(timeout: int = 3) -> list[tuple[str, str]]:
    # Create UDP socket
    scanner = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Enable UDP Broadcast
    scanner.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    # Wait maximum N seconds for responses
    scanner.settimeout(1)

    print("[DISCOVERY] Scanning network...")

    # Broadcast discovery request
    scanner.sendto(
        DISCOVERY_MESSAGE.encode(),
        ("255.255.255.255", DISCOVERY_PORT),
    )

    devices = []

    start_time = time()

    while time() - start_time < timeout:
        try:
            data, address = scanner.recvfrom(1024)

            response = data.decode()

            if not response.startswith(DISCOVERY_RESPONSE):
                continue

            _, hostname = response.split(":", 1)

            devices.append(
                (
                    hostname,
                    address[0],
                )
            )

        except TimeoutError:
            continue

    print()

    if not devices:
        print("[DISCOVERY] No Bebop devices found.")
        return

    print("Found Devices")
    print("-" * 40)

    for index, (hostname, ip) in enumerate(devices, start=1):
        print(f"{index}. {hostname:<20} {ip}")

    scanner.close()
    return devices


if __name__ == "__main__":
    discover_devices()

from bebop.core.discovery.scanner import (
    discover_devices,
)


def select_device() -> str:
    """
    Discover devices and let user select one.
    Returns selected IP address.
    """

    devices = discover_devices()

    if not devices:
        raise RuntimeError("No devices found")

    choice = int(input("\nSelect Device: "))

    hostname, ip = devices[choice - 1]

    print(f"\nSelected: {hostname} ({ip})")

    return ip

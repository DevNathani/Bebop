from datetime import datetime

from bebop.core.history.db import get_connection


def upsert_device(
    hostname: str,
    ip_address: str,
) -> None:
    connection = get_connection()

    cursor = connection.cursor()

    now = datetime.now().isoformat()

    cursor.execute(
        """
        SELECT id
        FROM devices
        WHERE hostname = ?
        """,
        (hostname,),
    )

    device = cursor.fetchone()

    if device:
        cursor.execute(
            """
            UPDATE devices
            SET
                ip_address = ?,
                last_seen = ?
            WHERE hostname = ?
            """,
            (
                ip_address,
                now,
                hostname,
            ),
        )

    else:
        cursor.execute(
            """
            INSERT INTO devices (
                hostname,
                ip_address,
                first_seen,
                last_seen
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                hostname,
                ip_address,
                now,
                now,
            ),
        )

    connection.commit()

    connection.close()


def get_devices() -> list[tuple]:
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            hostname,
            ip_address,
            first_seen,
            last_seen
        FROM devices
        ORDER BY last_seen DESC
        """
    )

    devices = cursor.fetchall()

    connection.close()

    return devices


def get_device(
    hostname: str,
) -> tuple | None:
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            hostname,
            ip_address,
            first_seen,
            last_seen
        FROM devices
        WHERE hostname = ?
        """,
        (hostname,),
    )

    device = cursor.fetchone()

    connection.close()

    return device


def delete_device(
    hostname: str,
) -> None:
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM devices
        WHERE hostname = ?
        """,
        (hostname,),
    )

    connection.commit()

    connection.close()


def device_exists(
    hostname: str,
) -> bool:
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT 1
        FROM devices
        WHERE hostname = ?
        """,
        (hostname,),
    )

    exists = cursor.fetchone() is not None

    connection.close()

    return exists

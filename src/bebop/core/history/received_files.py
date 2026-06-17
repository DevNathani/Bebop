from datetime import datetime

from bebop.core.history.db import get_connection


def save_received_file(
    filename: str,
    size: int,
    sender_name: str,
    sender_ip: str,
    status: str,
) -> None:
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO received_files (
            filename,
            size,
            sender_name,
            sender_ip,
            timestamp,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            filename,
            size,
            sender_name,
            sender_ip,
            datetime.now().isoformat(),
            status,
        ),
    )

    connection.commit()

    connection.close()


def get_received_history() -> list[tuple]:
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            filename,
            size,
            sender_name,
            sender_ip,
            timestamp,
            status
        FROM received_files
        ORDER BY timestamp DESC
        """
    )

    history = cursor.fetchall()

    connection.close()

    return history


def get_received_file(
    record_id: int,
) -> tuple | None:
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            filename,
            size,
            sender_name,
            sender_ip,
            timestamp,
            status
        FROM received_files
        WHERE id = ?
        """,
        (record_id,),
    )

    record = cursor.fetchone()

    connection.close()

    return record


def get_received_history_by_device(
    hostname: str,
) -> list[tuple]:
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            filename,
            size,
            sender_name,
            sender_ip,
            timestamp,
            status
        FROM received_files
        WHERE sender_name = ?
        ORDER BY timestamp DESC
        """,
        (hostname,),
    )

    history = cursor.fetchall()

    connection.close()

    return history

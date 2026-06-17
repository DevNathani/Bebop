from datetime import datetime

from bebop.core.history.db import get_connection


def save_sent_file(
    filename: str,
    size: int,
    receiver_name: str,
    receiver_ip: str,
    status: str,
) -> None:
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO sent_files (
            filename,
            size,
            receiver_name,
            receiver_ip,
            timestamp,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            filename,
            size,
            receiver_name,
            receiver_ip,
            datetime.now().isoformat(),
            status,
        ),
    )

    connection.commit()

    connection.close()


def get_sent_history() -> list[tuple]:
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            filename,
            size,
            receiver_name,
            receiver_ip,
            timestamp,
            status
        FROM sent_files
        ORDER BY timestamp DESC
        """
    )

    history = cursor.fetchall()

    connection.close()

    return history


def get_sent_file(
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
            receiver_name,
            receiver_ip,
            timestamp,
            status
        FROM sent_files
        WHERE id = ?
        """,
        (record_id,),
    )

    record = cursor.fetchone()

    connection.close()

    return record


def delete_sent_file(
    record_id: int,
) -> None:
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM sent_files
        WHERE id = ?
        """,
        (record_id,),
    )

    connection.commit()

    connection.close()


def clear_sent_history() -> None:
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM sent_files
        """
    )

    connection.commit()

    connection.close()


def get_sent_history_by_device(
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
            receiver_name,
            receiver_ip,
            timestamp,
            status
        FROM sent_files
        WHERE receiver_name = ?
        ORDER BY timestamp DESC
        """,
        (hostname,),
    )

    history = cursor.fetchall()

    connection.close()

    return history

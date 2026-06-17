import sqlite3

from bebop.config.config import DB_PATH


def get_connection() -> sqlite3.Connection:
    return sqlite3.connect(DB_PATH)


def init_db() -> None:
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS devices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            hostname TEXT NOT NULL UNIQUE,

            ip_address TEXT NOT NULL,

            first_seen TEXT NOT NULL,

            last_seen TEXT NOT NULL
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS sent_files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            filename TEXT NOT NULL,

            size INTEGER NOT NULL,

            receiver_name TEXT NOT NULL,

            receiver_ip TEXT NOT NULL,

            timestamp TEXT NOT NULL,

            status TEXT NOT NULL
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS received_files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            filename TEXT NOT NULL,

            size INTEGER NOT NULL,

            sender_name TEXT NOT NULL,

            sender_ip TEXT NOT NULL,

            timestamp TEXT NOT NULL,

            status TEXT NOT NULL
        )
        """
    )

    connection.commit()
    connection.close()


# def save_transfer(
#     filename: str,
#     size: int,
#     receiver: str,
#     status: str,
# ) -> None:
#     init_db()
#     print(f"[DB] Saving {filename}")

#     connection = sqlite3.connect(DB_PATH)

#     cursor = connection.cursor()

#     cursor.execute(
#         """
#         INSERT INTO transfers (
#             filename,
#             size,
#             receiver,
#             timestamp,
#             status
#         )
#         VALUES (?, ?, ?, ?, ?)
#         """,
#         (
#             filename,
#             size,
#             receiver,
#             datetime.now().isoformat(),
#             status,
#         ),
#     )

#     print(f"[DB] Rows affected: {cursor.rowcount}")

#     connection.commit()

#     print("[DB] Commit successful")

#     connection.close()

# def get_history() -> list[tuple]:
#     """
#     Fetch all transfer records.

#     Returns:
#         List of transfer rows ordered by
#         newest first.
#     """

#     connection = sqlite3.connect(DB_PATH)

#     cursor = connection.cursor()

#     cursor.execute(
#         """
#         SELECT
#             filename,
#             size,
#             receiver,
#             timestamp,
#             status
#         FROM transfers
#         ORDER BY id DESC
#         """
#     )

#     rows = cursor.fetchall()

#     connection.close()

#     return rows

# def show_history() -> None:
#     """
#     Display transfer history.
#     """

#     history = get_history()

#     if not history:
#         print(
#             "No transfer history found."
#         )
#         return

#     print("\nTransfer History")
#     print("-" * 60)

#     for (
#         filename,
#         size,
#         receiver,
#         timestamp,
#         status,
#     ) in history:

#         print(f"File     : {filename}")
#         print(f"Size     : {size} bytes")
#         print(f"Receiver : {receiver}")
#         print(f"Status   : {status}")
#         print(f"Time     : {timestamp}")

#         print("-" * 60)

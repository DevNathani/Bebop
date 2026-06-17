from bebop.core.history.db import get_history, init_db


def main() -> None:
    init_db()
    # show_history()
    history = get_history()

    print(f"Total Records: {len(history)}")

    for row in history:
        print(row)


if __name__ == "__main__":
    main()

import sqlite3


def main():
    connection = sqlite3.connect("./db/events.db")

    with open("db_script.sql") as f:
        connection.executescript(f.read())

    connection.close()


if __name__ == "__main__":
    main()

import sqlite3
import time


class DbConnectionManager():

    def __init__(self) -> None:
        super().__init__()
        self.db = sqlite3.connect('url.db', check_same_thread=False)
        self.sql = self.db.cursor()
        self.url_repo = UrlsBdRepository(self.db)
        self.sql.execute("""CREATE TABLE IF NOT EXISTS users (
            url TEXT,
            status INT,
            data INT
        ) """)
        self.sql.execute("""CREATE TABLE IF NOT EXISTS states (
            state INT
        ) """)

        self.db.commit()

    def get_url_repository(self):
        return self.url_repo


class UrlsBdRepository:
    def __init__(self, connection) -> None:
        super().__init__()
        self.connection = connection
        self.db = sqlite3.connect('url.db', check_same_thread=False)
        self.sql = self.db.cursor()

    def find_url(self, url):
        cursor = self.sql.execute(f"SELECT url FROM users WHERE  url = '{url}'")
        return cursor.fetchall()

    def check_and_recording_url_in_db(self, url, status, data):
        cursor = self.sql.execute(f"SELECT url FROM users WHERE  url = '{url}'")
        if cursor.fetchone() is None:
            self.sql.execute(f"INSERT INTO users VALUES(?,?,?)", (url, status, data))
            self.db.commit()
            return True
        return False

    def delete_element_in_db(self, number):
        cursor = self.sql.execute(f"SELECT url FROM users")
        all_urls = list(cursor.fetchall())
        if len(all_urls) <= number:
            return False
        else:
            concret_url = all_urls[number][0]
            self.sql.execute(f"DELETE FROM users WHERE url = '{concret_url}'")
            self.db.commit()
            return True

    def update_status(self, url: str, status: int, data: int):
        self.sql.execute(f"UPDATE users SET status = {status}, data = {data} WHERE url = '{url}'")
        self.db.commit()

    def all_info(self):
        cursor = self.db.execute(f"SELECT * FROM users")
        return list(cursor.fetchall())

    def get_state(self):
        cursor = self.sql.execute(f"SELECT state FROM states")
        all_states = list(cursor.fetchall())
        if len(all_states) == 0:
            return False
        return bool(all_states[0][0])

    def changing_state(self, state: bool):
        cursor = self.sql.execute(f"SELECT state FROM states")
        if cursor.fetchone() is None:
            self.sql.execute(f"INSERT INTO states (state) VALUES ({state})")
        else:
            self.sql.execute(f"UPDATE states SET state = {state}")
        self.db.commit()

    def all_urls(self):
        cursor = self.sql.execute(f"SELECT url FROM users")
        return cursor.fetchall()

import sqlite3


# импорт зависимости

class DbConnectionManager():
    # описание класса для работы с базой данных

    def __init__(self) -> None:
        # конструктор
        super().__init__()
        self.db = sqlite3.connect('../url.db', check_same_thread=False)
        # подключение к базе данных
        self.sql = self.db.cursor()
        # курсор
        self.url_repo = UrlsBdRepository(self.db)
        # экземпляр работы с самой базой данных
        self.sql.execute("""CREATE TABLE IF NOT EXISTS users (
            url TEXT,
            status INT,
            data INT,
            channel INT,
            chnl_name TEXT,
            category INT
        ) """)
        # описание первой таблицы
        self.sql.execute("""CREATE TABLE IF NOT EXISTS states (
            state INT
        ) """)
        # описание второй табоицы

        self.db.commit()
        # подтверждение действий в базе данных

    def get_url_repository(self):
        # получение экземпляра работы с самой базой данных
        return self.url_repo


class UrlsBdRepository:
    # описание класса с методами
    def __init__(self, connection) -> None:
        # конструктор
        super().__init__()
        self.connection = connection
        # подключение
        self.db = sqlite3.connect('../url.db', check_same_thread=False)
        # подключение к базе данных
        self.sql = self.db.cursor()
        # курсор

    def find_url(self, url):  # поиск url в базе данных
        cursor = self.sql.execute( f"SELECT url FROM users WHERE  url = '{url}'")
        # запрос на получение url из базы данных
        return cursor.fetchall()
        # выбор всех элементов

    def update_category(self, category):
        # обновление записе в базе данных о категориях
        self.sql.execute(f"UPDATE users SET category = {category} ")
        # запрос неа обновление записи в базе данных
        self.db.commit()  # подтверждение действий

    def update_channel_id(self, chnl_id, chnl_name):  # обновление id канала
        self.sql.execute(f"UPDATE users SET channel = {chnl_id} WHERE chnl_name = '{chnl_name}'")
        # запрос на обновление записи о канале
        self.db.commit()  # подтверждение действий

    def check_and_recording_url_in_db(self, url, status, data, chnl_id, chnl_name, category):
        # метод проверки и записи данных в базу данных
        cursor = self.sql.execute(f"SELECT url FROM users WHERE  url = '{url}'")
        # запрос на получение url из базы данных
        if cursor.fetchone() is None:
            # проверка на наличие записи в базе данных
            self.sql.execute(f"INSERT INTO users VALUES(?,?,?,?,?,?)",
                             (url, status, data, chnl_id, chnl_name, category))
            # запись информации в базу данных
            self.db.commit()
            # подтверждение действий
            return True
        return False

    def get_certain_record(self, number):
        cursor = self.sql.execute(f"SELECT * FROM users")
        # получение всех записей из базы данных
        all_urls = list(cursor.fetchall())
        # перевод в дургую стркутуру данных
        self.db.commit()
        # подтверждение действий
        if len(all_urls) <= number:
            # проверка на наличие искомой записи
            return False
        else:
            concret_url = all_urls[number][3]
            #  выбор конркетной записи из таблицы
            return concret_url

    def delete_element_in_db(self, number):
        #  метод на удаление элемента из базы данных
        cursor = self.sql.execute(f"SELECT url FROM users")
        # получение url из базы данных
        all_urls = list(cursor.fetchall())
        # перевод в другую струтурку данных
        if len(all_urls) <= number:
            # проверка на наличие записи
            return False
        else:
            concret_url = all_urls[number][0]
            # выбор конкретного элемента
            self.sql.execute(f"DELETE FROM users WHERE url = '{concret_url}'")
            # удаление записи из базы данных
            self.db.commit()
            # подтверждение действий
            return True

    def update_status(self, url: str, status: int, data: int):
        # обновление статуса ресурса
        self.sql.execute(f"UPDATE users SET status = {status}, data = {data} WHERE url = '{url}'")
        # запрос на обновление данных в базе данных
        self.db.commit()
        # подтверждение действий

    def all_info(self):
        # метож на получение всех записей в базе данных
        cursor = self.db.execute(f"SELECT * FROM users")
        # запрос на получение всех записей в базе данных
        return list(cursor.fetchall())
        # возврат всех элементов

    def get_state(self):
        # получение статуса ресурса
        cursor = self.sql.execute(f"SELECT state FROM states")
        # запрос на выбор статуса ресурса
        all_states = list(cursor.fetchall())
        # получение всех статусов
        if len(all_states) == 0:
            # проверка на наличие статусов
            return False
        return bool(all_states[0][0])
        # возврат всех статусов

    def changing_state(self, state: bool):
        # метод на изменение статуса в базе данных
        cursor = self.sql.execute(f"SELECT state FROM states")
        # выбор статуса
        if cursor.fetchone() is None:
            # проверка на наличие записис
            self.sql.execute(f"INSERT INTO states (state) VALUES ({state})")
            # запрос на новую запись в базе данных
        else:
            self.sql.execute(f"UPDATE states SET state = {state}")
            # запрос на обновление статуса
        self.db.commit()
        # подтверждение действий в базе данных

    def all_urls(self):
        # метод получения всех url
        cursor = self.sql.execute(f"SELECT url FROM users")
        # запрос на получение всех url в базе данных
        return cursor.fetchall()
        # возврат всех url

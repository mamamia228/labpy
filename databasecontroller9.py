# controllers/databasecontroller.py
# тут база SQLite в памяти и простой execute
# старался сделать понятно: один метод execute и все

import sqlite3


class DatabaseController:
    def __init__(self):
        self.conn = sqlite3.connect(":memory:", check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self._init_tables()

    def _init_tables(self):
        # Таблица пользователей
        self.cursor.execute("""
        CREATE TABLE user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
        """)

        # Таблица валют
        self.cursor.execute("""
        CREATE TABLE currency (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            num_code TEXT,
            char_code TEXT,
            name TEXT,
            value REAL,
            nominal INTEGER
        )
        """)

        # Связь пользователь-валюта
        self.cursor.execute("""
        CREATE TABLE user_currency (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            currency_id INTEGER,
            FOREIGN KEY(user_id) REFERENCES user(id),
            FOREIGN KEY(currency_id) REFERENCES currency(id)
        )
        """)
        self.conn.commit()

    def execute(self, sql, params=(), commit=False, fetch_one=False, fetch_all=False):
        #  параметры через ? это защита от SQL-инъекций
        self.cursor.execute(sql, params)

        if commit:
            self.conn.commit()

        if fetch_one:
            r = self.cursor.fetchone()
            return dict(r) if r else None

        if fetch_all:
            rows = self.cursor.fetchall()
            return [dict(x) for x in rows]

        # если вставка, вернем id
        if sql.strip().upper().startswith("INSERT"):
            return int(self.cursor.lastrowid)

        return None

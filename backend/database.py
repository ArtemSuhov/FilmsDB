import sqlite3
import logging
import csv
from typing import Any, List, Tuple

class Database:
    def __init__(self, filename):
        self.filename = filename

    def sql_do(self, sql: str, params: Tuple[Any, ...] = ()):
        try:
            cur = self._db.cursor()
            cur.execute(sql, params)
            self._db.commit()
            logging.debug("Successfully executed SQL query: %s with parameters %r", sql, params)

        except sqlite3.Error as e:
            logging.error("Failed to execute SQL query: %s", e)
            raise e


    def db_select(self, sql: str, params: Tuple[Any, ...] = ()) -> List[Tuple]:
        try:
            cur = self._db.cursor()
            cur.execute(sql, params)
            logging.debug("Successfully executed SQL query: %s with parameters %r", sql, params)

            return cur.fetchall()
        except sqlite3.Error as e:
            logging.error("Failed to fetch data from database: %s", e)
            raise e


    def fill_from_csv(self, csv_path: str, tablename: str):
        with open(csv_path, 'r', encoding="Windows-1251") as file:
            reader = csv.reader(file, delimiter=";")
            next(reader)  # Skip header row

            try:
                cur = self._db.cursor()
                cur.executemany(f"INSERT INTO {tablename} VALUES (?, ?, ?)", reader)
                self._db.commit()
                logging.debug("Successfully filled data from CSV to table: %s", tablename)
            except sqlite3.Error as e:
                self._db.rollback()
                logging.error("Failed to fill data from CSV to table: %s", e)
                raise e


    def execute_script_file(self, script_file: str):
        with open(script_file, 'r') as file:
            sql_script = file.read()
            sql_commands = sql_script.split(';')

            try:
                cur = self._db.cursor()
                for command in sql_commands:
                    if command.strip():
                        cur.execute(command)
                self._db.commit()
                logging.debug("Successfully executed SQL script from file: %s", script_file)

            except sqlite3.Error as e:
                logging.error("Failed to execute SQL script from file: %s", e)
                raise e

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, fn):
        self._filename = fn
        self._db = sqlite3.connect(fn, check_same_thread=False)
        self._db.row_factory = sqlite3.Row


    def __del__(self):
        self._db.close()
        del self._filename

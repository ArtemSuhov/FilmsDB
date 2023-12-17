import sqlite3
import logging
import pandas as pd


class Database:
    def __init__(self, filename):
        self.filename = filename

    def sql_do(self, sql, params):
        try:
            cur = self._db.cursor()
            cur.execute(sql, params)
            self._db.commit()
            logging.info("Удачно запущен sql скрипт  " + sql + " с параметрами " + str(params))

        except sqlite3.OperationalError as e:
            logging.error("Не удалось получить список из базы данных")
            raise e

    def db_select(self, sql, params):
        try:
            cur = self._db.cursor()
            cur.execute(sql, params)
            logging.info("Удачно запущен sql скрипт " + sql + " с параметрами " + str(params))

            return cur.fetchall()
        except Exception as e:
            logging.error("Не удалось получить список из базы данных")

    def fill_from_csv(self, csv_path, tablename):
        reader = pd.read_csv(csv_path, delimiter=";", encoding="Windows-1251")
        try:
            reader.to_sql(tablename, self._db, if_exists="replace", index=False)
        except sqlite3.OperationalError as e:
            self._db.rollback()
            logging.error("Вставка в базу данных не удалась")

        self._db.commit()

    def execute_script_file(self, script_file):
        with open(script_file, 'r') as file:
            sql_script = file.read()
            sql_commands = sql_script.split(';')

            try:
                for command in sql_commands:
                    if command.strip():
                        self.sql_do(command)
                logging.info("Удачно запущен sql скрипт из файла" + script_file)

            except sqlite3.OperationalError as e:
                logging.error("Ошибка запуска скрипта из файла" + script_file)
                raise e

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, fn):
        self._filename = fn
        self._db = sqlite3.connect(fn, check_same_thread=False)
        self._db.row_factory = sqlite3.Row

    @filename.deleter
    def filename(self):
        self.close()

    def close(self):
        self._db.close()
        del self._filename

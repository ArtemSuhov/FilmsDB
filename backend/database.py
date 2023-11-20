import sqlite3
import csv
import pandas as pd


class Database:
    def __init__(self, filename):
        self.filename = filename

    def sql_do(self, sql):
        try:
            self._db.cursor().execute(sql)
            self._db.commit()
            # log "Execution successful"

        except sqlite3.OperationalError as e:
            # log "error wit operations"
            self._db.rollback()
            raise

    def db_select(self, sql):
        try:
            return self._db.cursor().execute(sql).fetchall()
        except Exception as e:
            self._db.rollback()
            # log Failed to fetch values

    def fill_from_csv(self, csv_path, tablename):
        reader = pd.read_csv(csv_path, delimiter=";", encoding="Windows-1251")
        try:
            reader.to_sql(tablename, self._db, if_exists="replace", index=False)
        except sqlite3.OperationalError as e:
            self._db.rollback()
            print("failed")
            # log error
        self._db.commit()

    def execute_script_file(self, script_file):
        with open(script_file, 'r') as file:
            sql_script = file.read()
            sql_commands = sql_script.split(';')

            try:
                for command in sql_commands:
                    if command.strip():
                        self.sql_do(command)
                # log "Execution succesfull"

            except sqlite3.OperationalError as e:
                # log "error wit operations"
                self._db.rollback()
                raise

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

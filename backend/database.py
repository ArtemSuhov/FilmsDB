import sqlite3
import csv

class Database:
    def __init__(self, **kwargs):
        self.filename = kwargs.get('filename')

    def sql_do(self, sql, *params):
        try:
            self._db.execute(sql, params)
            self._db.commit()
            # log "Execution successful"

        except sqlite3.OperationalError as e:
            # log "error wit operations"
            self._db.rollback()
            raise

    def db_select(self, sql, *values):
        try:
            self.sql_do(sql, values)
            return self._db.cursor().fetchall()
        except Exception as e:
            self._db.rollback()
            #log Failed to fetch values


    def fill_from_csv(self, csv_path, tablename):
        data_set = set()
        with open(csv_path, 'r') as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                data_set.add(row[0])
        for entry in data_set:
            query = f"INSERT IGNORE INTO {tablename} (name) VALUES (%s)"
            values = (entry,)
            try:
                self._db.cursor().execute(query, values)
            except sqlite3.OperationalError as e:
                self._db.rollback()
                #log error
        self._db.commit()

    def execute_script_file(self, script_file):
        with open(script_file, 'r') as file:
            sql_script = file.read()
            sql_commands = sql_script.split(';')

            try:
                for command in sql_commands:
                    if command.strip():
                        self.sql_do(command)
                #log "Execution succesfull"

            except sqlite3.OperationalError as e:
                #log "error wit operations"
                self._db.rollback()
                raise
    @property
    def filename(self): return self._filename
    @filename.setter
    def filename(self, fn):
        self._filename = fn
        self._db = sqlite3.connect(fn)
        self._db.row_factory = sqlite3.Row
    @filename.deleter
    def filename(self): self.close()

    def close(self):
            self._db.close()
            del self._filename
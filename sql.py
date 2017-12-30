import sqlite3


class SQLConnect:
    def __init__(self, db="dnd.db"):
        self.open = False
        self.db = db

    def __enter__(self):
        self.connect()

    def __exit__(self):
        self.close()

    def connect(self):
        if self.open:
            print("Already connected to DB '{}'".format(self.db))
        else:
            self.connection = sqlite3.connect(self.db)
            self.cursor = self.connection.cursor()
            print("Connected to DB '{}'".format(self.db))
            self.open = True

    def close(self):
        self.connection.close()
        self.open = False
        print("Connection to '{}' has been closed.".format(self.db))

    def create_table(self, table_name, field_name, field_type, pk=False):
        if not self.open:
            print("Not currently connected to a DB.")
            return False
        try:
            if pk:
                pk = " PRIMARY KEY"

            q = 'CREATE TABLE IF NOT EXISTS {tn}({fn} {ft}{pk})'
            self.cursor.execute(q.format(tn=table_name,
                                         fn=field_name,
                                         ft=field_type,
                                         pk=pk))
        except Exception as e:
            print("Table not created: \n{}".format(e))
            return False


    def add_field(self, table_name, field_name, field_type, pk="", default=""):
        if not self.open:
            print("Not currently connected to a DB.")
            return False
        try:
            if pk:
                pk = " PRIMARY KEY"

            if default:
                default = " DEFAULT '{}'".format(default)

            q = "ALTER TABLE {tn} ADD COLUMN '{fn}' {ft}{df}{pk}"
            self.cursor.execute(q.format(tn=table_name,
                                         fn=field_name,
                                         ft=field_type,
                                         pk=pk,
                                         df=default))
        except Exception as e:
            print("Table not created: \n{}".format(e))
            return False

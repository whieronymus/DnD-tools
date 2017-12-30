import sqlite3
import traceback
import pdb


def print_exc_plus(tb):
    """
    -------------------------------------------------------------------------
    This isn't my code, I stole it from the internet because I needed to take
    a closer look at some of the tracebacks, we probably don't need it going
    forward, but I'll keep it around for a bit to debug.
    --------------------------------------------------------------------------
    Print the usual traceback information, followed by a listing of all the
    local variables in each frame.
    """
    while 1:
        if not tb.tb_next:
            break
        tb = tb.tb_next
    stack = []
    f = tb.tb_frame
    while f:
        stack.append(f)
        f = f.f_back
    stack.reverse()
    traceback.print_exc()
    print("Locals by frame, innermost last")
    for frame in stack:
        print()
        print("Frame %s in %s at line %s" % (frame.f_code.co_name,
                                             frame.f_code.co_filename,
                                             frame.f_lineno))
        for key, value in frame.f_locals.items():
            print("\t%20s = " % key,)
            #We have to be careful not to cause a new error in our error
            #printer! Calling str() on an unknown object could cause an
            #error we don't want.
            try:
                print(value)
            except:
                print("<ERROR WHILE PRINTING VALUE>")


class SQLConnect:
    def __init__(self, db="dnd.db"):
        self.open = False
        self.db = db
        self.query = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            print(exc_type, exc_value, traceback)
            print_exc_plus(traceback)
            # pdb.set_trace()
        self.close()
        return self

    def __str__(self):
        prefix = "<SQLite3 Connection> Status: "
        if self.open:
            str_ = "Connected to {}"
        else:
            str_ = "Not currently connected to {}"

        return prefix + str_.format(self.db)

    def __repr__(self):
        return self.__str__()

    def connect(self):
        if self.open:
            print("Already connected to DB '{}'".format(self.db))
        else:
            self.connection = sqlite3.connect(
                self.db,
                detect_types=sqlite3.PARSE_DECLTYPES
            )
            sqlite3.register_adapter(bool, int)
            sqlite3.register_converter("BOOLEAN", lambda v: bool((v)))
            self.connection.row_factory = self.dict_factory
            self.cursor = self.connection.cursor()
            print("Connected to DB '{}'".format(self.db))
            self.open = True

    def close(self):
        self.connection.close()
        self.open = False
        print("Connection to '{}' has been closed.".format(self.db))

    def create_table(self, table_name):
        """
        Creates a new Table with an ID PK field in the DB.

        Takes one variable (str) 'table_name' that will become the
        name of the new Table

        Table is automatically created with an ID field as the Primary Key

        Returns True on success, False on any error
        """
        if not self.open:
            print("Not currently connected to a DB.")
            return False

        q = '''CREATE TABLE
        IF NOT EXISTS {tn}
        (ID INTEGER PRIMARY KEY)'''
        self.query = q.format(tn=table_name)

        try:
            self.cursor.execute(self.query)
            print("{} table created.".format(table_name))
            self.connection.commit()
            return True
        except Exception as error:
            print("Unable to create '{}' table.".format(table_name))
            print("SQL Query: \n{}\n".format(self.query))
            print("Exception: \n{}".format(error))

            return False


    def add_field(self, table_name, field_name, field_type,
                  pk="", default="", not_null=""):
        """
        Creates a new field on an existing table in the DB.
        Takes an existing table name, a field name for the new column,
        field type, default value, and a boolean to determine whether or not
        new field is a PK and/or should except NULL values.

        NOT NULL fields require a default value
        Cannot add a new Unique field, you'll have to update the field after.

        Returns True on Success, False on any error.

        Example:
        db.add_field("races", "spped", "INT", default=30)
        """
        if not self.open:
            print("Not currently connected to a DB.")
            return False

        if pk:
            pk = " PRIMARY KEY"

        if not_null:
            not_null = " NOT NULL"

        if not default == "":
            default = " DEFAULT '{}'".format(default)

        q = "ALTER TABLE {tn} ADD '{fn}' {ft}{df}{pk}{nn}"
        self.query = q.format(tn=table_name,
                                   fn=field_name,
                                   ft=field_type,
                                   pk=pk,
                                   df=default,
                                   nn=not_null)

        try:
            self.cursor.execute(self.query)
            print("{} column added to {} table.".format(field_name, table_name))
            self.connection.commit()
            return True
        except Exception as error:
            print("Failed to add {} to {} table.".format(field_name, table_name))
            print("SQL Query: \n{}\n".format(self.query))
            print("Exception: \n{}".format(error))

            return False

    def add_record(self, table_name, **kwargs):
        """
        Creates a new Record in the given Table.
        Takes a table name and keyword arguments matching the existing
        columns in the DB.

        Example:
        db.add_record("races",
                      name="Drow",
                      str=0,
                      wis=1,
                      dex=2,
                      con=0,
                      chr=0.
                      int=0)
        """

        if not self.open:
            print("Not currently connected to a DB.")
            return False


        fields = ", ".join('"{}"'.format(f) for f in kwargs.keys())
        values = ", ".join('"{}"'.format(v) for v in kwargs.values())
        q = "INSERT INTO {tn}({columns}) VALUES ({values})"
        self.query = q.format(tn=table_name,
                              columns=fields,
                              values=values)

        try:
            self.cursor.execute(self.query)
            self.connection.commit()
            print("{}\n inserted into {} table.".format(values, table_name))
            return True
        except Exception as error:
            print("Failed to add {} to {} table.".format(values, table_name))
            print("SQL Query: \n{}\n".format(self.query))
            print("Exception: \n{}".format(error))

            return False


    def dict_factory(self, cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def select(self, table_name, **kwargs):
        """
        Selects data from Table
        Takes 'table_name' and kwargs as filters

        Example:
        db.select('races') <-- grabs all races from races table
        db.select('races', speed=30) <-- grabs all races with a speed of 30 
        """
        if not self.open:
            print("Not currently connected to a DB.")
            return False

        where_claus = ""
        if kwargs:
            filters = " AND ".join(["{} = '{}'".format(k, v)
                                   for k, v in kwargs.items()])
            where_claus = "WHERE {}".format(filters)

        q = """SELECT * FROM {tn} {wh}"""
        self.query = q.format(tn=table_name,
                              wh=where_claus)

        try:
            self.cursor.execute(self.query)
            rows = self.cursor.fetchall()
            return rows
        except Exception as error:
            print("Problem with Query.")
            print("SQL Query: \n{}\n".format(self.query))
            print("Exception: \n{}".format(error))

            return False

# # no context manager, I have to manually close the file with f.close()
# f = open('helloworld.txt','r')
# message = f.read()
# print(message)
# f.close()

# # with context manager, I don't have to close the file, it's automatically
# # closed at the end of "with"
# with open('helloworld.txt', 'r') as f:
#     message = f.read()
#     print(message)



# def create_table():
#     # Use all caps for SQL, regular casing for nonSQL
#     c.execute(
#         'CREATE TABLE IF NOT EXISTS character_data(keyword TEXT, value REAL)'
#     )


# def data_entry(keyword, data_input):
#     # KYLE: There is almost never a valid reason to use \ to split lines
#     # Any [], {}, () can be split after a comma without using \
#     # \ isn't technically wrong, it's just ugly
#     c.execute(
#         "INSERT INTO character_data(keyword, value) VALUES (?, ?)",
#         (keyword, data_input)
#     )
#     print(data_input)
#     conn.commit()

# def delete_data():
#     c.execute('DELETE FROM character_data WHERE keyword = "Background"')
#     conn.commit()

# create_table()

# class_list = ['Barbarian', 'Bard', 'Druid', 'Fighter', 'Monk', 'Ranger',
#               'Rogue', 'Sorcerer', 'Warlock', 'Wizard']
# race_list = ['Hill Dwarf', 'Mountain Dwarf', 'Drow', 'High Elf', 'Wood Elf',
#              'Lightfoot Halfling', 'Stout Halfling', 'Human', 'Dragonborn',
#              'Forest Gnome', 'Rock Gnome', 'Half-Elf', 'Half-Orc', 'Tiefling']
# background_list = ['Acolyte', 'Charlatan', 'Criminal', 'Entertainer',
#                    'Folk Hero', 'Guild Artisan', 'Hermit', 'Noble',
#                    'Outlander', 'Sage', 'Sailor', 'Soldier', 'Urchin']
# for i in background_list:
#     data_entry('Background', i)


# c.close
# conn.close()

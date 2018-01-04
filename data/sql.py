import sqlite3
import traceback
import inspect
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

    def connect(self, get_db=True):
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
            self.open = True

            if get_db:
                print("get_db")
                self.get_sql()
                self.DB = DB(self.db, query_result=self.sql)

            print("Connected to DB '{}'".format(self.db))


    def check_connection(self):
        if not self.open:
            print("Not currently connected to a DB.")
            reconnect = input("Reconnect (y/n)?:  ")

            if reconnect.lower() in ['y', 'yes']:
                self.connect()
                return True

            else:
                info = inspect.stack()
                caller = info[1][3]

                print("Calling Function: sql.{}".format(caller))
                print("Pending queries will not be executed.")
                return False

        else:
            return True

    def close(self):
        self.connection.close()
        self.open = False
        print("Connection to '{}' has been closed.".format(self.db))

    def get_sql(self):
        if not self.check_connection():
            return False

        self.query = "SELECT * FROM sqlite_master WHERE type='table'"

        try:
            self.cursor.execute(self.query)
            rows = self.cursor.fetchall()
            self.sql = rows
            return True

        except Exception as error:
            print("Cannot get DB raw SQL")
            print("SQL Query: \n{}\n".format(self.query))
            print("Exception: \n{}".format(error))

            return False


    def create_table(self, table=None, table_name=None):
        """
        Creates a new Table with an ID PK field in the DB.

        Takes one variable (str) 'table_name' that will become the
        name of the new Table

        Table is automatically created with an ID field as the Primary Key

        Returns True on success, False on any error
        """
        if not self.check_connection():
            return False

        if table:
            self.query = table.get_sql()
            table_name = table.name

        elif raw_sql:
            self.query = raw_sql

        elif table_name:
            q = '''CREATE TABLE
            IF NOT EXISTS {tn}
            (id INTEGER PRIMARY KEY{fields})'''
            self.query = q.format(tn=table_name)

        else:
            print("Please pass in a Table object, a raw sql create statement,")
            print("Or a just a table name to create a blank table.")

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
        if not self.check_connection():
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

    def add_unique_contraint(self, table_name, fields):
        """
        Adds a unique index to the given table

        The field or fields passed in will uniquely identify a record
        in the passed in table.

        This will prevent (will throw sqlite3.ItegrityError) duplicate records
        from being created in the table.
        """

        if not self.check_connection():
            return False

        field_names = ", ".join('"{}"'.format(f) for f in fields)
        unique_name = "_".join(f for f in fields)

        q = "CREATE UNIQUE INDEX {un} {tn}({fn})"
        self.query = q.format(un=unique_name,
                              tn=table_name,
                              fn=field_name)

        try:
            self.cursor.execute(self.query)
            print("Unique index {} added to {} table.".format(unique_name,
                                                              table_name))
            self.connection.commit()
            return True
        except Exception as error:
            print("Failed to add unique index to {} table.".format(field_name,
                                                                   table_name))
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

        if not self.check_connection():
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
        if not self.check_connection():
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


class DB:
    def __init__(self, file_name, query_result=None):
        self.name = file_name
        self.sql_query = query_result
        self.tables = {}
        if query_result:
            self.generate_schema(query_result=query_result)

    def generate_schema(self, query_result):
        for table in query_result:
            sql = table['sql']
            name = table['tbl_name']
            self.tables[name] = Table(name=name, raw_sql=sql)

    @property
    def schema(self):
        print()
        for table in self.tables.values():
            print('TABLE: {}'.format(table.name))



class Table:
    def __init__(self, name=None, raw_sql=None):
        self.name = name
        self.sql = raw_sql
        self.fields = []

        if raw_sql:
            self.generate_schema(raw_sql)

    def __repr__(self):
        return "Table({})".format(self.name)

    @property
    def schema(self):
        print('\nTABLE: {}'.format(self.name))
        for field in self.fields:
            print(field.schema)

    def get_sql(self):
        fields = ",\n".join([f.schema for f in self.fields])
        fks = ",\n".join([f.fk_schema for f in self.fields if f.fk])
        t = """CREATE TABLE {n} (
            {f}{if_fks}{fks}\n)"""

        if fks:
            if_fks = ",\n"
        else:
            fks = ""
            if_fks = ""

        return t.format(n=self.name,
                        f=fields,
                        if_fks=if_fks,
                        fks=fks)

    def generate_schema(self, raw_sql):
        create_table, _, fields = raw_sql[:-1].partition('(')
        fks = [f for f in fields.split(", ") if f.startswith("FOREIGN KEY")]
        fk_dict = {}
        for fk in fks:
            fk_str = fk.split('(')[1]
            field_last = fk_str.find(')')
            fk_field = fk_str[:field_last]
            fk_table = fk_str.split("REFERENCES ")[1]
            fk_dict[fk_field] = fk_table


        field_list = fields.split(", ")
        for field_sql in field_list:
            fk = None
            name = field_sql.split()[0].strip("'")
            if name == "FOREIGN":
                break
            if name in fk_dict.keys():
                fk = fk_dict(name)
            self.fields.append(Field(name=name, raw_sql=field_sql, fk=fk))


class Field:
    FIELD_TYPES = ['INT', 'INTEGER', 'TEXT', 'BLOB', 'REAL', 'BOOLEAN',
                   'FLOAT', 'NUMERIC', 'DATE', 'DATETIME', 'FK', None]

    def __init__(self, raw_sql=None, name=None, pk=False, fk=None, not_null=False,
                 autoincrement=False, unique=False, default=None, ftype=None):
        self.name = name
        self.table = None
        self.pk = pk
        self.fk = fk
        self.not_null = not_null
        self.autoincrement = autoincrement
        self.unique = unique
        self.default = default
        self.ftype = self._validate_type(ftype)
        if raw_sql:
            self.generate_schema(raw_sql)

    def __repr__(self):
        return "Field(name={}, raw_sql={})".format(self.name, self.schema)

    def __str__(self):
        return self.schema

    def _validate_type(self, ftype):
        if ftype in self.FIELD_TYPES:
            return ftype
        else:
            pdb.set_trace()
            raise AttributeError("{} is not a valid Field Type".format(ftype))

    @property
    def schema(self):
        if self.pk:
            pk = " PRIMARY KEY"
        else:
            pk = ""
        if self.autoincrement:
            auto = " AUTOINCREMENT"
        else:
            auto = ""
        if self.default:
            df = " DEFAULT '{}'".format(self.default)
        else:
            df = ""
        if self.unique:
            unq = " UNIQUE"
        else:
            unq = ""
        if self.not_null:
            nn = " NOT NULL"
        else:
            nn = ""
        if self.fk:
            self.ftype == 'INT'


        t = "'{n}' {t}{pk}{a}{d}{u}{nn}".format(n=self.name,
                                                t=self.ftype,
                                                pk=pk,
                                                a=auto,
                                                d=df,
                                                u=unq,
                                                nn=nn)
        return t

    @property
    def fk_schema(self):
        if self.fk:
            t = "FOREIGN KEY({}) REFERENCES {}('id')".format(self.name, self.fk)
            return t
        else:
            return None

    def generate_schema(self, sql=None):
        keywords = sql.split()
        self.name = keywords[0].strip("'")
        self.ftype = self._validate_type(keywords[1])
        if "PRIMARY KEY" in sql:
            self.pk = True
        if "AUTOINCREMENT" in sql:
            self.autoincrement = True
        if "UNIQUE" in sql:
            self.unique = True
        if "NOT NULL" in sql:
            self.not_null = True
        if "DEFAULT" in sql:
            *_, default = sql.partition('DEFAULT ')
            self.default = default.split("'")[1]

"""
CREATE TABLE races (
    'id' INTEGER PRIMARY KEY,
    'base_race' TEXT DEFAULT 'RACE' NOT NULL,
    'sub_race' TEXT,
    'source' TEXT DEFAULT 'PHB' NOT NULL,
    'name' TEXT DEFAULT 'RACE' NOT NULL,
    'base_height' INTEGER DEFAULT '12' NOT NULL,
    'height_mod' TEXT DEFAULT '1d1' NOT NULL,
    'base_weight' INTEGER DEFAULT '12' NOT NULL,
    'weight_mod' TEXT DEFAULT '1d1' NOT NULL,
    'speed' INTEGER DEFAULT '30' NOT NULL,
    'str_bonus' INTEGER DEFAULT '0' NOT NULL,
    'dex_bonus' INTEGER DEFAULT '0' NOT NULL,
    'con_bonus' INTEGER DEFAULT '0' NOT NULL,
    'int_bonus' INTEGER DEFAULT '0' NOT NULL,
    'wis_bonus' INTEGER DEFAULT '0' NOT NULL,
    'cha_bonus' INTEGER DEFAULT '0' NOT NULL,
    'languages' TEXT DEFAULT 'Common' NOT NULL,
    'trait_1' TEXT,
    'trait_2' TEXT,
    'trait_3' TEXT,
    'trait_4' TEXT,
    'trait_5' TEXT,
    'trait_6' TEXT,
    'trait_7' TEXT,
    'trait_8' TEXT
)
"""

"""
CREATE TABLE background_characteristics (
    id INTEGER PRIMARY KEY,
    'background' TEXT DEFAULT 'Acolyte' NOT NULL,
    'characteristic' TEXT DEFAULT 'Trait' NOT NULL,
    'alignment' TEXT,
    'description' TEXT
)
"""

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

from sql import SQLConnect, DB, Table, Field
from gsheets import GSheet
import csv
import pdb
import os

clear = lambda: os.system('cls')
clear()

g = GSheet()

race_table = Table('races')
race_gsheet = g.get_table_fields('races')
races = g.get_table_records('races')
race_table.create_fields_from_gsheet(race_gsheet)

class_table = Table('classes')
class_gsheet = g.get_table_fields('classes')
classes = g.get_table_records('classes')
class_table.create_fields_from_gsheet(class_gsheet)

background_table = Table('backgrounds')
background_gsheet = g.get_table_fields('backgrounds')
backgrounds = g.get_table_records('backgrounds')
background_table.create_fields_from_gsheet(background_gsheet)

with SQLConnect('dnd2.db') as db:
    db.create_table(race_table)
    db.create_table(class_table)
    db.create_table(background_table)

    for race in races:
        db.add_record(table_name='races', **race)

    for cclass in classes:
        db.add_record(table_name='classes', **cclass)

    for background in backgrounds:
        db.add_record(table_name='classes', **background)



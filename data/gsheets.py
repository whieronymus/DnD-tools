# Get Data from Google Sheets

# Standard Libary
import pdb
import sys

# 3rd Party
import gspread
from oauth2client.service_account import ServiceAccountCredentials

from sql import Table, Field, SQLConnect

scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    'gsheetcreds.json', scope)

gclient = gspread.authorize(credentials)

dnd = gclient.open('dnddb')
t = dnd.worksheet("races")

col_names = t.row_values(1)
empty_columns = "" in col_names
if empty_columns:
    print("remove extra columns from sheet and try again.")
    sys.exit()

new_table = Table('races5')

db_params = ['name',
             'ftype',
             'fk'
             'pk',
             'not_null',
             'autoincrement',
             'unique',
             'default']

for col in range(2, len(col_names) + 1):
    values = t.col_values(col)[:8]
    field = Field(name=values[0],
                  ftype=values[1],
                  fk=values[2],
                  pk=bool(values[3]),
                  not_null=bool(values[4]),
                  autoincrement=bool(values[5]),
                  unique=bool(values[6]),
                  default=values[7])
    new_table.fields.append(field)

pdb.set_trace()
with SQLConnect('dnd.db') as db:
    db.create_table(new_table)


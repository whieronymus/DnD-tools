# Get Data from Google Sheets

# Standard Libary
import pdb
import sys
from collections import namedtuple

# 3rd Party
import gspread
from oauth2client.service_account import ServiceAccountCredentials

from sql import Table, Field, SQLConnect

scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    'gsheetcreds.json', scope)


class GSheet:
    def __init__(self):
        self.client = gspread.authorize(credentials)
        self.wb = self.client.open('dnddb')
        self.sheets = self.wb.worksheets()
        self.test_sheets()


    def test_sheets(self):
        for sheet in self.sheets:
            ready =  self.sheet_ready(sheet=sheet, all_sheets=True)
            if not ready[0]:
                print("SHEET:", sheet.title)
                print("{} extra columns".format(ready[1][0]))
                print("{} extra rows".format(ready[1][1]))
            else:
                print("SHEET: {} READY".format(sheet.title))

    def sheet_ready(self, sheet_name=None, sheet=None, all_sheets=False):
        if sheet_name:
            sheet = self.wb.worksheet(sheet_name)
        
        columns = sheet.row_values(1)
        rows = sheet.row_values(2)[9:]
        empty_cols = [c for c in columns if not c]
        empty_rows = [r for r in rows if not r]
        ready = not empty_cols and not empty_rows

        if all_sheets:
            if ready:
                return (True,)
            else:
                return (False, (len(empty_cols), len(empty_rows)))

        else:
            if not ready:
                print("{} extra columns".format(len(empty_cols)))
                print("{} extra rows".format(len(empty_rows)))
            return ready

    def get_table_fields(self, sheet_name=None):
        if not self.sheet_ready(sheet_name):
            return False

        sheet = self.wb.worksheet(sheet_name)
        name = sheet.row_values(1)[1:]
        ftype = sheet.row_values(2)[1:]
        fk = sheet.row_values(3)[1:]
        pk = sheet.row_values(4)[1:]
        not_null = sheet.row_values(5)[1:]
        autoinc = sheet.row_values(6)[1:]
        unique = sheet.row_values(7)[1:]
        default = sheet.row_values(8)[1:]
        field_list = []
        for i, n in enumerate(name):
            field = {}
            field['name'] = name[i]
            field['ftype'] = ftype[i]
            field['fk'] = fk[i]
            field['pk'] = pk[i]
            field['not_null'] = not_null[i]
            field['autoincrement'] = autoinc[i]
            field['unique'] = unique[i]
            field['default'] = default[i]
            field_list.append(field)

        return field_list

    def get_table_records(self, sheet_name=None):
        if not self.sheet_ready(sheet_name):
            return False

        sheet = self.wb.worksheet(sheet_name)
        recs = sheet.get_all_records()[8:]
        for rec in recs:
            rec.pop('COLUMN NAME')
            rec.pop('id')

        return recs

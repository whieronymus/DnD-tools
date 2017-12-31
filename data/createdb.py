from sql import SQLConnect
import csv
import pdb
import os

clear = lambda: os.system('cls')
clear()

def create_tables(debug=False):
    with SQLConnect('dnd.db') as db:
        # Create Race Table
        table = db.create_table('races')

        if table:
            db.add_field('races', 'base_race', 'TEXT', default="RACE", not_null=True)
            db.add_field('races', 'sub_race', 'TEXT')
            db.add_field('races', 'source', 'TEXT', default="PHB", not_null=True)
            db.add_field('races', 'name', 'TEXT', default="RACE", not_null=True)
            db.add_field('races', 'base_height', 'INTEGER', default=12, not_null=True)
            db.add_field('races', 'height_mod', 'TEXT', default='1d1', not_null=True)
            db.add_field('races', 'base_weight', 'INTEGER', default=12, not_null=True)
            db.add_field('races', 'weight_mod', 'TEXT', default='1d1', not_null=True)
            db.add_field('races', 'speed', 'INTEGER', default=30, not_null=True)
            db.add_field('races', 'str_bonus', 'INTEGER', default=0, not_null=True)
            db.add_field('races', 'dex_bonus', 'INTEGER', default=0, not_null=True)
            db.add_field('races', 'con_bonus', 'INTEGER', default=0, not_null=True)
            db.add_field('races', 'int_bonus', 'INTEGER', default=0, not_null=True)
            db.add_field('races', 'wis_bonus', 'INTEGER', default=0, not_null=True)
            db.add_field('races', 'cha_bonus', 'INTEGER', default=0, not_null=True)
            db.add_field('races', 'languages', 'TEXT', default="Common", not_null=True)
            db.add_field('races', 'trait_1', 'INTEGER')
            db.add_field('races', 'trait_2', 'INTEGER')
            db.add_field('races', 'trait_3', 'INTEGER')
            db.add_field('races', 'trait_4', 'INTEGER')
            db.add_field('races', 'trait_5', 'INTEGER')
            db.add_field('races', 'trait_6', 'INTEGER')
            db.add_field('races', 'trait_7', 'INTEGER')
            db.add_field('races', 'trait_8', 'INTEGER')

            # Test Race Table
            if debug:
                success = db.add_record('races',
                                        base_race='Dwarf',
                                        sub_race='Hill',
                                        name='Hill Dwarf',
                                        min_height=46,
                                        max_height=57,
                                        speed=25,
                                        str_bonus=0,
                                        dex_bonus=0,
                                        con_bonus=2,
                                        int_bonus=0,
                                        wis_bonus=1,
                                        cha_bonus=0,
                                        trait_1=6,
                                        trait_2=15,
                                        trait_3=16,
                                        trait_4=41,
                                        trait_5=36,
                                        trait_6=17,
                                        trait_7=None,
                                        trait_8=None,)


                if success:
                    print("'Race' Table tested successfully.")
                else:
                    print("Failed to create new 'Race' record.")

                print('\n\n\n')


        # Create Character Name Table
        table = db.create_table('names')
        if table:
            db.add_field('names', 'name', 'TEXT', default="Jerry", not_null=True)
            db.add_field('names', 'race_id', 'INTEGER', default=1, not_null=True)
            db.add_field('names', 'gender', 'TEXT')
            db.add_field('names', 'region', 'TEXT')
            db.add_field('names', 'is_child', 'BOOLEAN', default=False, not_null=True)
            db.add_field('names', 'is_given', 'BOOLEAN', default=True, not_null=True)
            db.add_field('names', 'is_nickname', 'BOOLEAN', default=False, not_null=True)
            db.add_field('names', 'is_family', 'BOOLEAN', default=False, not_null=True)

            if debug:
                # Test Name Table
                success = db.add_record('names',
                                        name='Adrik',
                                        race_id='1',
                                        gender='M',
                                        region=None,
                                        is_child=False,
                                        is_given=True,
                                        is_nickname=False,
                                        is_family=False)

                if success:
                    print("'Name' Table tested successfully.")
                else:
                    print("Failed to create new 'Name' record.")

                print('\n\n\n')



def load_races():
    with open('csv_data/races.csv', 'r') as f:
        csv_data = csv.reader(f)
        print(next(csv_data))
        races = [row for row in csv_data]

    with SQLConnect('dnd.db') as db:
        for race in races:
            try:
                db.add_record('races',
                              base_race=race[1],
                              sub_race=race[2],
                              source=race[3],
                              name=race[4],
                              base_height=race[5],
                              height_mod=race[6],
                              base_weight=race[7],
                              weight_mod=race[8],
                              speed=race[9],
                              str_bonus=race[10],
                              dex_bonus=race[11],
                              con_bonus=race[12],
                              int_bonus=race[13],
                              wis_bonus=race[14],
                              cha_bonus=race[15],
                              trait_1=race[16],
                              trait_2=race[17],
                              trait_3=race[18],
                              trait_4=race[19],
                              trait_5=race[20],
                              trait_6=race[21],
                              trait_7=race[22],
                              trait_8=race[23],)
                print("{} created!".format(race[4]))
            except sqlite3.IntegrityError:
                print("{} already exists.".format(race[4]))


if __name__ == '__main__':
    create_tables()
    load_races()

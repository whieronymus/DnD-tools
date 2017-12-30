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
            db.add_field('races', 'name', 'TEXT', default="RACE", not_null=True)
            db.add_field('races', 'min_height', 'INTEGER', default=12, not_null=True)
            db.add_field('races', 'max_height', 'INTEGER', default=120, not_null=True)
            db.add_field('races', 'speed', 'INTEGER', default=30, not_null=True)
            db.add_field('races', 'str_bonus', 'INTEGER', default=0, not_null=True)
            db.add_field('races', 'dex_bonus', 'INTEGER', default=0, not_null=True)
            db.add_field('races', 'con_bonus', 'INTEGER', default=0, not_null=True)
            db.add_field('races', 'chr_bonus', 'INTEGER', default=0, not_null=True)
            db.add_field('races', 'int_bonus', 'INTEGER', default=0, not_null=True)
            db.add_field('races', 'wis_bonus', 'INTEGER', default=0, not_null=True)
            db.add_field('races', 'languages', 'TEXT', default="Common", not_null=True)
            db.add_field('races', 'trait_1', 'TEXT')
            db.add_field('races', 'trait_2', 'TEXT')
            db.add_field('races', 'trait_3', 'TEXT')
            db.add_field('races', 'trait_4', 'TEXT')
            db.add_field('races', 'trait_5', 'TEXT')
            db.add_field('races', 'trait_6', 'TEXT')
            db.add_field('races', 'trait_7', 'TEXT')
            db.add_field('races', 'trait_8', 'TEXT')

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
                                        chr_bonus=0,
                                        int_bonus=0,
                                        wis_bonus=1,
                                        trait_1="Darkvision",
                                        trait_2="Dwarven Resilience",
                                        trait_3="Dwarven Combat Training",
                                        trait_4="Tool Proficiency",
                                        trait_5="Stonecunning",
                                        trait_6="Dwarven Toughness",
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
                              name=race[3],
                              min_height=race[4],
                              max_height=race[5],
                              speed=race[6],
                              str_bonus=race[7],
                              dex_bonus=race[8],
                              con_bonus=race[9],
                              chr_bonus=race[10],
                              int_bonus=race[11],
                              wis_bonus=race[12],
                              trait_1=race[13],
                              trait_2=race[14],
                              trait_3=race[15],
                              trait_4=race[16],
                              trait_5=race[17],
                              trait_6=race[18],
                              trait_7=race[19],
                              trait_8=race[20],)
                print("{} created!".format(race[3]))
            except sqlite3.IntegrityError:
                print("{} already exists.".format(race[3]))


if __name__ == '__main__':
    create_tables()
    load_races()

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
                                        source='PHB',
                                        name='Hill Dwarf',
                                        base_height=46,
                                        height_mod='1d1',
                                        base_weight=110,
                                        weight_mod='1d1',
                                        speed=25,
                                        str_bonus=0,
                                        dex_bonus=0,
                                        con_bonus=2,
                                        int_bonus=0,
                                        wis_bonus=1,
                                        cha_bonus=0,
                                        languages='Common',
                                        trait_1='Darkvision',
                                        trait_2='Dwarven Combat Training',
                                        trait_3='Dwarven Resilience',
                                        trait_4='Tool Proficiency',
                                        trait_5='Stonecunning',
                                        trait_6='Stout Resilience',
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
            db.add_field('names', 'translation', 'TEXT')

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
                                        is_family=False,
                                        translation='Moonunit')


                if success:
                    print("'Name' Table tested successfully.")
                else:
                    print("Failed to create new 'Name' record.")

                print('\n\n\n')


        # Create Background Table
        table = db.create_table('backgrounds')
        if table:
            db.add_field('backgrounds', 'background', 'TEXT', default="Acolyte", not_null=True)
            db.add_field('backgrounds', 'source', 'TEXT', default='PHB', not_null=True)
            db.add_field('backgrounds', 'skill1', 'TEXT')
            db.add_field('backgrounds', 'skill2', 'TEXT')
            db.add_field('backgrounds', 'languages', 'TEXT')
            db.add_field('backgrounds', 'tool_proficiency', 'TEXT')
            db.add_field('backgrounds', 'equipment', 'TEXT')

            if debug:
                # Test Name Table
                success = db.add_record('backgrounds',
                                        background='Hermit',
                                        source='PHB',
                                        skill1='Medicine',
                                        skill2='Religion',
                                        languages='One of your choice',
                                        tool_proficiency='Herbalism Kit',
                                        equipment='A scroll case stuffed full of notes from your studies or prayers, a winter blanket, a set of common clothes, a herbalism kit, and 5 gp')

                if success:
                    print("'Background' Table tested successfully.")
                else:
                    print("Failed to create new 'Background' record.")

                print('\n\n\n')


        # Create Background Characteristics Table
        table = db.create_table('background_characteristics')
        if table:
            db.add_field('background_characteristics', 'background', 'TEXT', default="Acolyte", not_null=True)
            db.add_field('background_characteristics', 'characteristic', 'TEXT', default='Trait', not_null=True)
            db.add_field('background_characteristics', 'alignment', 'TEXT')
            db.add_field('background_characteristics', 'description', 'TEXT')

            if debug:
                # Test Name Table
                success = db.add_record('background_characteristics',
                                        background='Acolyte',
                                        characteristic='Type',
                                        alignment=None,
                                        description="I idolize a particular hero of my faith, and constantly refer to that person's deeds and example.",)

                if success:
                    print("'background_characteristics' Table tested successfully.")
                else:
                    print("Failed to create new 'background_characteristics' record.")

                print('\n\n\n')


def load_races():
    with open('csv_data/races.csv', 'r') as f:
        csv_data = csv.reader(f)
        # Skips first line
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
                              languages=race[16],
                              trait_1=race[17],
                              trait_2=race[18],
                              trait_3=race[19],
                              trait_4=race[20],
                              trait_5=race[21],
                              trait_6=race[22],
                              trait_7=race[23],
                              trait_8=race[24],)
                print("{} created!".format(race[4]))
            except sqlite3.IntegrityError:
                print("{} already exists.".format(race[4]))


def load_names():
    with open('csv_data/names.csv', 'r') as f:
        csv_data = csv.reader(f)
        print(next(csv_data))
        names = [row for row in csv_data]

    with SQLConnect('dnd.db') as db:
        for name in names:
            try:
                db.add_record('names',
                              name=name[1],
                              race_id=name[2],
                              gender=name[3],
                              region=name[4],
                              is_child=name[5],
                              is_given=name[6],
                              is_nickname=name[7],
                              is_family=name[8],
                              translation=name[9])

                print("{} created!".format(name[1]))
            except sqlite3.IntegrityError:
                print("{} already exists.".format(name[1]))


def load_backgrounds():
    with open('csv_data/backgrounds.csv', 'r') as f:
        csv_data = csv.reader(f)
        print(next(csv_data))
        backgrounds = [row for row in csv_data]

    with SQLConnect('dnd.db') as db:
        for background in backgrounds:
            try:
                db.add_record('backgrounds',
                              background=background[1],
                              source=background[2],
                              skill1=background[3],
                              skill2=background[4],
                              languages=background[5],
                              tool_proficiency=background[6],
                              equipment=background[7])

                print("{} created!".format(background[1]))
            except sqlite3.IntegrityError:
                print("{} already exists.".format(background[1]))

def load_background_characteristics():
    with open('csv_data/background_characteristics.csv', 'r') as f:
        csv_data = csv.reader(f)
        print(next(csv_data))
        background_characteristics = [row for row in csv_data]

    with SQLConnect('dnd.db') as db:
        for background_characteristic in background_characteristics:
            try:
                db.add_record('background_characteristics',
                              background=background_characteristic[1],
                              characteristic=background_characteristic[2],
                              alignment=background_characteristic[3],
                              description=background_characteristic[4])

                print("{} created!".format(background_characteristic[1]))
            except sqlite3.IntegrityError:
                print("{} already exists.".format(background_characteristic[1]))


if __name__ == '__main__':
    create_tables()
    # load_races()
    load_names()
    # load_backgrounds()
    # load_background_characteristics()

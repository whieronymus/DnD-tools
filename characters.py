import pdb
from data.sql import SQLConnect
from pprint import pprint as pp
import random


class Character:
    def __init__(self, all_random=True):
        self.all_random = all_random
        with SQLConnect() as self.db:
            self.races = self.db.select('races')
            self.select_race()
            # self.classes = self.db.select('classes')


    def select_race(self):

        if self.all_random:
            self.race = random.choice(self.races)
        else:
            for race in self.races:
                print("{}. {}".format(race['ID'], race['name']))

            print("\nSelect a Race from the options above!")
            print("(Enter a Number corresponding with the Race you want")
            race_selected = input("CHOICE>> ")
            self.race = filter(lambda x: x.get('ID') == race_selected,
                                                        self.races)
            pdb.set_trace()

        print("Selected Race: {}".format(self.race['name']))





    def select_class(self):
        pass

    def roll_stats(self):
        pass
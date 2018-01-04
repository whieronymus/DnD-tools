# Standard Library
import pdb
from pprint import pprint as pp
from random import choice as random_choice

# Local App
from data.sql import SQLConnect
from utils import Dice





class CharacterBuilder:
    def __init__(self):
        with SQLConnect("data/dnd.db") as self.db:
            self.races = self.db.select('races')
            self.classes = self.db.select('classes')
            self.backgrounds = self.db.select('backgrounds')

    def create_character(self, random=True):
        self.select_race(random=random)
        self.select_class(random=random)
        self.roll_ability_scores(random=random)

    def select_race(self, random):

        if random:
            self.race = random_choice(self.races)
        else:
            for race in self.races:
                print("{}. {}".format(race['ID'], race['name']))

            print("\nSelect a Race from the options above!")
            print("(Enter a Number corresponding with the Race you want")
            race_selected = input("CHOICE>> ")
            self.race = self.races[int(race_selected) - 1]

        print("Selected Race: {}".format(self.race['name']))

    def select_class(self, random):

        if random:
            self.char_class = random_choice(self.classes)
        else:
            for char_class in self.classes:
                print("{}. {}".format(char_class['ID'], char_class['class_name']))

            print("\nSelect a Class from the options above.")
            print("(Enter a Number corresponding with the Class you want")
            class_selected = input("CHOICE>> ")
            self.char_class = self.classes[int(class_selected) - 1]

        print("Selected Class: {}".format(self.char_class['class_name']))

    def roll_ability_scores(self, random):
        ability_scores = sorted([Dice.roll_and_drop()[0] for stat in range(6)],
                                reverse=True)

        if random:
            stats = ['STR', 'DEX', 'CON', 'INT', 'WIS', 'CHA']
            self.ability_scores = dict(zip([s.upper() for s in stats],
                                           ability_scores))

        else:
            self.ability_scores = {}
            stats = ['STR', 'DEX', 'CON', 'INT', 'WIS', 'CHA']
            race_bonus = [self.race['str_bonus'],
                          self.race['dex_bonus'],
                          self.race['con_bonus'],
                          self.race['int_bonus'],
                          self.race['wis_bonus'],
                          self.race['cha_bonus']]

            while ability_scores:
                stat_display = [s + '(+{})'.format(race_bonus[i])
                for i, s in enumerate(stats)]
                print("Remaining stats:", stat_display)
                print("Remaining ability scores:", ability_scores)
                stat = input('Select stat for highest ability score')

                if stat.upper() in stats:
                    stats.remove(stat.upper())
                    self.ability_scores[stat.lower()] = ability_scores.pop(0)




x = CharacterBuilder()
x.create_character(random=False)

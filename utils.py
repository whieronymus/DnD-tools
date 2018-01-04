from random import randint

class Dice:

    @staticmethod
    def roll_and_drop(dice_str=None, sides=6, dice=4, drop=1):
        """
        Rolls x dice, drops the lowest x results and sums the total

        Takes either a dice_str ("4d6", "2d20", "3d10") or the number of
        sides and dice as integers, followed by the number of dropped dice.

        Returns a Tuple
        (INT: Sum of Kept Dice, LIST: Kept Dice, LIST: Dropped Dice)

        To just get the total back, call like this:
        total = Dice.roll_and_drop()[0]
        """
        if dice_str:
            dice, sides = [int(num) for num in dice_str.split("d")]

        roll = sorted(randint(1, sides) for d in range(dice))
        dropped = roll[:drop]
        kept = roll[drop:]
        total = sum(kept)
        return total, kept, dropped

    @staticmethod
    def roll(dice_str=None, dice=1, sides=6):
        """
        Rolls x dice sums the total

        Takes either a dice_str ("4d6", "2d20", "3d10") or the number of
        sides and dice as integers

        Returns the total as an INT
        """
        if dice_str:
            dice, sides = [int(num) for num in dice_str.split("d")]

        return sum([randint(1, sides) for d in range(dice)])

    @staticmethod
    def d20():
        """
        Rolls a single 20 sided die and returns the result

        prints "Critical Miss or Hit" on a 1 or 20 roll
        """
        roll = randint(1, 20)
        if roll == 1:
            print("CRITICAL MISS!")
        elif roll == 20:
            print("CRTIICAL HIT!")
        return roll




from random import randint

def roll_stats():
    """
    Returns a list of 6 stats from highest to lowest
    These stats are built by rolling 4d6, dropping the lowest
    Then addings the remaining 3 together
    """
    returnValues = []
    for j in range(6):
        rollList = []
        for i in range(4):
            rollList.append(randint(1,6))
        rollList.sort()
        del rollList[0]
        returnValues.append(sum(rollList))
    returnValues.sort(reverse=True)
    return returnValues


def roll_dice(dice_str):
    dice, sides = [int(num) for num in dice_str.split("d")]
    return sum([randint(1, sides) for d in range(dice)])



def roll_dice2(dice_str):
    dice_vals = dice_str.split("d")
    dice = int(dice_vals[0])
    sides = int(dice_vals[1])

    total = 0
    for die in range(dice):
        roll = randint(1, sides)
        total += roll

    return total


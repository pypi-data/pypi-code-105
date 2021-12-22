from typing import List
from random import choice, randrange
from games_box.utils.animals import ANIMALS
from games_box.utils.colours import COLOURS


class RollResult:
    def __init__(self, die_name: str, result: int):
        self.die_name = die_name
        self.result = result

    def __repr__(self) -> str:
        return f"{self.die_name}: {self.result}"


class RollResultsPool:
    def __init__(self, rolls: List[RollResult]):
        self.rolls = rolls
        self.total = self.__sum()

    def __sum(self):
        total = 0

        for roll in self.rolls:
            total = total + roll.result

        return total

    def __repr__(self) -> str:
        result_string = ""
        for roll in self.rolls:
            result_string = result_string + f"{roll.die_name}: {roll.result}\n"
        result_string = result_string + f"Total: {self.total}"
        return result_string


class Die:
    def __init__(self, sides: int, name: str = None):
        self.__validate_sides(sides)
        self.sides = sides
        self.name = name or self.__generate_friendly_name()

    def roll(self) -> RollResult:
        return RollResult(self.name, randrange(1, self.sides))

    def __generate_friendly_name(self):
        return generate_die_name(self.sides)

    @staticmethod
    def __validate_sides(sides: int):
        assert isinstance(sides, int)
        assert sides > 0


class DicePool:
    def __init__(self, dice: List[Die]):
        self.dice = dice

    def roll(self) -> RollResultsPool:
        rolls = []
        for die in self.dice:
            rolls.append(die.roll())

        return RollResultsPool(rolls)


def args_to_dice(args: List[str]):
    dice = []
    for arg in args:
        parts = arg.split("-")

        sides = int(parts[0])
        name = parts[1] if len(parts) > 1 else None

        dice.append(Die(sides, name))
    return dice


def pick_colour() -> str:
    return choice(COLOURS)


def pick_animal() -> str:
    return choice(ANIMALS)


def generate_die_name(sides: int) -> str:
    return f"d{sides}-{pick_colour()}-{pick_animal()}"

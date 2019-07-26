from typing import List, Dict, Tuple
from enum import Enum
# Player has three main phases:
# 1. Troop allocation
# 2. Attacking phases
# 3. Fortification phase(1 move)


class Player:
    def __init__(self, name):
        self.name = name


class Country:
    owner: Player = None
    units: int = 0

    def __init__(self, name: str, adj: List[str]):
        self.name = name
        self.adj = adj

    def conquer(self, conquerer: Player):
        self.owner = conquerer


class Continent:
    owner = None

    def __init__(self, name: str, countries: List[Country], reward: int):
        # Name of continent and ownership reward
        self.name = name
        self.reward = reward
        self.countries = countries


class Game:
    class Turn(Enum):
        Placement = 1
        Attack = 2
        Fortify = 3

    turn = {
        "player": None,
        "step": Turn.Placement
    }

    def __init__(self, cards):
        self.cards = cards

    def attack(self, attacker, defender) -> bool:
        return True

    def fortify(self, fro, to):
        return True

    def place(self, num):
        return True

    def nextStep(self):
        return True


class CardUnit(Enum):
    Soldier = 1
    Horse = 2
    Canon = 3
    WildCard = 4


class Card:
    location = None
    unit = None

    def __init__(self, unit: CardUnit, location: Country):
        self.unit = unit
        if unit != CardUnit.WildCard:
            self.location = location


class Deck:
    cards = []

    def __init__(self, cards):
        self.cards = cards

    def pop(self):
        return self.cards.pop()

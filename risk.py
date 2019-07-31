from typing import List, Dict, Tuple
from enum import Enum
from random import shuffle
from math import floor
import random
# Player has three main phases:
# 1. Troop allocation
# 2. Attacking phases
# 3. Fortification phase(1 move)


class Player:
    free_units = 0

    def __init__(self, name, free_units=0):
        self.name = name
        self.free_units = free_units

    def __repr__(self):
        return "{}, {}".format(self.name, self.free_units)


class Country:
    owner: Player = None
    units: int = 0

    def __init__(self, name: str, adj: List[str]):
        self.name = name
        self.adj = adj

    def conquer(self, conquerer: Player):
        self.owner = conquerer

    def __repr__(self):
        return "{}, {} units, {}".format(self.name, self.units, self.owner.name)


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

    state = {
        "player": None,
        "step": Turn.Placement
    }
    tiles = {}
    continents = {}
    deck = None
    players = []

    def __init__(self, config):
        self.continents = {}
        for continent, countryDict in config['countries'].items():
            ContCountries = []
            for countryName, neighbours in countryDict.items():
                newCountry = Country(
                    name=countryName,
                    adj=neighbours)
                ContCountries.append(newCountry)
                self.tiles[newCountry.name] = newCountry

            self.continents[continent] = Continent(
                name=continent,
                countries=ContCountries,
                reward=config['contvals'][continent])
        cards = []
        for card in config['cards']:
            cards.append(Card(*card))
        self.deck = Deck(cards)

        for player in config['players']:
            self.players.append(Player(player['name'], player['troops']))

        if config['style']['init_allocation'] == "uniform_random":
            idx = 0
            tiles_per_player = len(self.tiles)/len(self.players)
            # Find average amount of units to add to a tile on init
            units_per_tile = {player.name: {
                "min": floor(player.free_units/tiles_per_player),
                "remain": int(player.free_units - tiles_per_player*floor(player.free_units/tiles_per_player))
            }
                for player
                in self.players}
            print(units_per_tile)
            for _, tile in self.tiles.items():
                tile.owner = self.players[idx % len(self.players)]
                # randomly allocate either one more or one less to tile to
                units_to_tile = units_per_tile[tile.owner.name]['min']
                # Eat up remainder troops near beginning of loop
                if units_per_tile[tile.owner.name]['remain'] > 0:
                    units_to_tile += 1
                    units_per_tile[tile.owner.name]['remain'] -= 1
                # Add units to the tile. If no units left, use remainder
                if tile.owner.free_units >= units_to_tile:
                    tile.owner.free_units -= units_to_tile
                    tile.units += units_to_tile
                else:
                    tile.units += tile.owner.free_units
                    tile.owner.free_units = 0
                idx += 1

    def attack(self, attacker, defender) -> bool:
        raise NotImplementedError

    def fortify(self, fro, to):
        raise NotImplementedError

    def place(self, num):
        raise NotImplementedError

    def next_step(self):
        raise NotImplementedError

    def _validateInput(self):
        raise NotImplementedError

    def game_over(self):
        owners = []
        for continent in self.continents.values():
            owners.append(continent.owner)
        return all(owner == owners[0] and owner != None for owner in owners)


class CardUnit(Enum):
    Soldier = 1
    Horse = 2
    Cannon = 3
    WildCard = 4


class Card:
    location = None
    unit = None

    def __init__(self, location, unit):

        self.location = Game.tiles[location] if location else None
        self.unit = {
            "Horse": CardUnit.Horse,
            "Soldier": CardUnit.Soldier,
            "Cannon": CardUnit.Cannon,
            "WildCard": CardUnit.WildCard
        }[unit]


class Deck:
    cards = []

    def __init__(self, cards: List[Card]):
        self.cards = cards

    def pop(self):
        return self.cards.pop()

    def shuffle(self):
        shuffle(self.cards)

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


class Step(Enum):
    Placement = 1
    Attack = 2
    Fortify = 3


class Turn:
    """
    This class holds all the state associated with
    which state we are currently in.
    """

    def __init__(self, players: List[Player]):
        self.curr = players[0]
        self.players = players
        self.step = Step.Placement

    def __repr__(self):
        if self.step == Step.Placement:
            return "{} may place {} units".format(self.curr.name, self.curr.free_units)
        elif self.step == Step.Attack:
            return "{} may attack".format(self.curr.name)
        elif self.step == Step.Fortify:
            return "{} may fortify once".format(self.curr.name)
        else:
            return "Invalid state..."


class Game:

    turn = None
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

        # by default first player in array begins turn, can be changed in config
        self.turn = Turn(self.players)

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

    def place(self, player: Player, num: int, tile: str):
        if tile not in self.tiles:
            raise KeyError("Invalid tile given as input.")
        elif self.turn.curr.free_units < num:
            raise ValueError("Trying to place toot many units.")
        elif self.turn.curr == player and \
                self.turn.step == Step.Placement and \
                self.turn.curr.free_units >= num and \
                self.tiles[tile].owner == player:
            self.tiles[tile].units += num
            return
        raise NotImplementedError

    def get_players(self):
        return self.players

    def query_action(self):
        return str(self.turn)

    def next_step(self):
        if self.turn.step == Step.Placement and \
                self.turn.curr.free_units == 0:
            self.turn.step = Step.Attack
        if self.turn.step == Step.Attack:
            self.turn.step = Step.Fortify
        if self.turn.step == Step.Fortify:

            # need to calc placement number
            self.turn.curr = self.turn.players[
                self.turn.players.index(
                    self.turn.curr) + 1 % len(self.turn.players)
            ]
            self.turn.step = Step.Placement

    def _validateInput(self):
        raise NotImplementedError

    def _get_num_place(self, player: Player):
        new_units = 0
        tot_tiles = 0
        for tile in self.tiles:
            if tile.owner == player:
                tot_tiles += 1
        # 1 extra unit per 3 territories
        new_units == floor(tot_tiles / 3)
        for continent in self.continents:
            if continent.owner == player:
                new_units += continent.reward
        if new_units < 3:
            new_units = 3
        return new_units

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

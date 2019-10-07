from typing import List, Dict, Tuple
from enum import Enum
from random import shuffle
from math import floor
import random
from players import Player, Human, Machine
# Player has three main phases:
# 1. Troop allocation
# 2. Attacking phases
# 3. Fortification phase(1 move)


class Country:
    owner: Player = None
    units: int = 0

    def __init__(self, name: str, adj: List[str]):
        self.name = name
        self.adj = adj

    def conquer(self, conquerer: Player):
        self.owner = conquerer

    def __repr__(self):
        return "Country({}, {}, {})".format(self.name, self.units, self.owner)


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

    def next_state(self, game):
        if self.step == Step.Placement:
            if self.curr.free_units == 0:
                self.step = Step.Attack
            else:
                raise ValueError("Player still has units to place")
        elif self.step == Step.Attack:
            self.step = Step.Fortify
        elif self.step == Step.Fortify:
            self.curr = self.players[self.players.index(self.curr) + 1]
            self.step = Step.Placement
            self.curr.refill_troops(game.tiles, game.continents)


class Game:

    turn: Turn = None
    tiles: Dict[str, Country] = {}
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
            if player['type'] == "Human":
                self.players.append(Human(player['name'], player['troops']))
            elif player['type'] == "Machine":
                self.players.append(Machine(player['name'], player['troops']))

        if config['playstyle']['init_allocation'] == "uniform_random":
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
        elif config['playstyle']['init_allocation'] == "manual":
            # Players can pick where to place units on turn at beginning
            pass

            # by default first player in array begins turn, can be changed in config
        self.turn = Turn(self.players)
        self.turn.curr.refill_troops(self.tiles, self.continents)

    def attack(self, attacker, defender) -> bool:
        raise NotImplementedError

    def fortify(self, fro, to):
        raise NotImplementedError

    def place(self, player: Player, num: int, tile: str):
        if tile not in self.tiles:
            raise KeyError("Invalid tile given as input.")
        elif self.turn.curr.free_units < num:
            raise ValueError("Trying to place too many units.")
        elif self.tiles[tile].owner != player:
            raise ValueError("You do not own this tile.")
        elif self.turn.curr == player and \
                self.turn.step == Step.Placement and \
                self.turn.curr.free_units >= num and \
                self.tiles[tile].owner == player:
            player.free_units -= num
            self.tiles[tile].units += num
            if self.turn.curr.free_units == 0:
                self.turn.next_state(self)
            return
        raise NotImplementedError

    def get_players(self):
        return self.players

    def query_action(self):
        return str(self.turn)

    def _validate_input(self):
        raise NotImplementedError

    def game_over(self):
        owners = []
        for continent in self.continents.values():
            owners.append(continent.owner)
        return all(owner == owners[0] and owner != None for owner in owners)

    def play(self):
        while not self.game_over():
            # Add optional loop for manually placing troops at beginning
            print(self.query_action())
            if self.turn.step == Step.Placement:
                free_land = {k: v for k, v in self.tiles.items()
                             if v.owner == None}  # What if all countries are owned, stop while
                if len(free_land) > 0:
                    # if there are still unowned tiles, next player must place there
                    terr, num = self.turn.curr.placement_control(free_land)
                    self.place(self.turn.curr, num, terr)
                else:
                    # if all tiles are owned by a player, you must place on your own tiles
                    owned_land = {k: v for k, v in self.tiles.items()
                                  if v.owner == self.turn.curr}
                    self.turn.curr.placement_control(owned_land)
            elif self.turn.step == Step.Attack:
                terr = input("Country to attack: ")

        # Risk.attack()


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

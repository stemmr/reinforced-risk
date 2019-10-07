from math import floor


class Player:
    free_units = 0

    def __init__(self, name, free_units=0):
        self.name = name
        self.free_units = free_units

    def __repr__(self):
        return "Player({}, {})".format(self.name, self.free_units)

    def refill_troops(self, tiles, continents):
        new_units = 0
        tot_tiles = 0
        for tile in tiles.values():
            if tile.owner == self:
                tot_tiles += 1
        # 1 extra unit per 3 territories
        new_units == floor(tot_tiles / 3)
        for continent in continents.values():
            if continent.owner == self:
                new_units += continent.reward
        if new_units < 3:
            new_units = 3
        self.free_units += new_units

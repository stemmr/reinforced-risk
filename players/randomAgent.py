from .player import Player
import random


class RandomAgent(Player):
    """
    A Random player, randomly selects moves
    """

    def __init__(self, name, troops):
        super().__init__(name, troops)

    def placement_control(self, placeable, units, querystyle="default"):
        ch = random.choice(list(placeable.keys())), random.randint(1, units)
        return ch

    def attack_control(self, att_lines):
        # 25% of the time dont attack
        if random.random() > 0.75 or att_lines == []:
            return None, None
        ch = random.choice(att_lines)
        return ch[0], ch[1]

    def fortify_control(self, fort_lines):
        # 10% of the time don't fortify
        # print(fort_lines)
        if random.random() > 0.9 or len(fort_lines) == 0:
            return None, None, 0
        fline = random.choice(fort_lines)
        num = random.randint(0, fline[0].units - 1)
        return fline[0], fline[1], num

    def overtaking_tile(self, num_units):
        return random.choice(num_units)

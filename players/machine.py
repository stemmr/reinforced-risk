from .player import Player


class Machine(Player):
    """
    A Machine player, should be capable of handling learned actions autonomously
    all functionality should be in Player, where this just provides a way to act as a player 
    """

    def __init__(self, name, troops):
        super.__init__(name, troops)

    def placement_control(self, placeable, querystyle="default"):
        pass

    def attack_control(self, att_lines):
        pass

    def fortify_control(self, fort_lines):
        pass

    def overtaking_tile(self, num_units):
        pass

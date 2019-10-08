from .player import Player


class Human(Player):
    """
    A Human player, provides a way to control via CLI or (later) GUI
    all functionality should be in Player, where this just provides a way to act as a player 
    """

    def __init__(self, name, troops):
        super().__init__(name, troops)

    def placement_control(self, placeable, querystyle="default"):
        """
        Abstracts how a user should be queried where to place units 
        should also create attack_control and fortify_control
        """
        print("Pick one of:", '\n')
        for c in placeable.keys():
            print(c, end='\t')
        print('\n')
        terr = input("Country to place: ")
        if querystyle == "default":
            num = int(input("Number of troops: "))
        else:
            num = 1

        return terr, num
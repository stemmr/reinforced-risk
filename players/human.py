from .player import Player


class Human(Player):
    """
    A Human player, provides a way to control via CLI or (later) GUI
    all functionality should be in Player, where this just provides a way to act as a player 
    """

    def __init__(self, name, troops):
        super().__init__(name, troops)

    def placement_control(self, r):
        try:
            terr = input("Country to place: ")
            num = int(input("Number of troops: "))
            r.place(r.turn.curr, num, terr)
        except KeyError as e:
            print(e)
            self.placement_control(r)
        except ValueError as e:
            print(e)
            self.placement_control(r)

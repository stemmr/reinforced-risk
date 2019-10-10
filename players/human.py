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

    def attack_control(self, att_lines):
        print("Pick an attack line:")
        for line in att_lines:
            print(
                f"{line[0].name}({line[0].units}) -> {line[1].name}({line[1].units})", end="\t")
        print("\n")
        fro = input("Attacking from: ")
        to = input("Attacking to: ")
        if to == '' and fro == '':
            # additional option not to attack
            # of course we would prefer a peaceful world!
            return None, None
        for att, defn in att_lines:
            if att.name == fro and defn.name == to:
                return att, defn
        raise ValueError("That is an invalid attack line, pick another please")

    def fortify_control(self, fort_lines):
        print("pick a fortify line:")
        for line in fort_lines:
            print(f"{line[0]} -> {line[1]}")
        ffro = input("Fortify from: ")
        fto = input("Fortify to: ")
        num = int(input("Number of units: "))
        print("\n")
        if ffro == '' or fto == '':
            return None, None, 0
        for fro, to in fort_lines:
            if ffro == fro and fto == to:
                return ffro, fto, num
        raise ValueError(
            "That is an invalid fortify line, pick another please")

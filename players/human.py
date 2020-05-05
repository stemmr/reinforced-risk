from .player import Player


class Human(Player):
    """
    A Human player, provides a way to control via CLI or (later) GUI
    all functionality should be in Player, where this just provides a way to act as a player 
    """

    def __init__(self, name, troops, context):
        super().__init__(name, troops, context)

    def placement_control(self, placeable, state, querystyle="default"):
        """
        Abstracts how a user should be queried where to place units 
        should also create attack_control and fortify_control
        ignore number of units if passed
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

    def attack_control(self, att_lines, state):
        print("Pick an attack line:")
        for idx, line in enumerate(att_lines):
            if idx % 3 == 0:
                print("\n")
            op = f"{line[0].name}({line[0].units}) -> {line[1].name}({line[1].units})".ljust(30)
            print(op, end="\t")
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

    def fortify_control(self, fort_lines, state):
        print("pick a fortify line:")
        for line in fort_lines:
            print(f"{line[2]} units {line[0].name} -> {line[1].name}")
        ffro = input("Fortify from: ")
        fto = input("Fortify to: ")
        num = int(input("Number of units: "))
        print("\n")
        if ffro == '' or fto == '':
            return None, None, 0
        for fro, to, n_units in fort_lines:
            if ffro == fro.name and fto == to.name and num == n_units:
                return fro, to, num
        raise ValueError(
            "That is an invalid fortify line, pick another please")

    def overtaking_tile(self, num_units, state):
        print("You won an attack!")
        print(num_units)
        uns = int(input("pick a number of units to move: "))
        if uns <= 0 or uns > num_units[-1]:
            raise ValueError(f"{uns} is not a valid number of units to move")
        return uns

from risk import Game, Step
import json


def main():
    # Main control loop of Risk
    # https://www.alternatehistory.com/forum/threads/risk%C2%AE-maps.66855/
    # https://www.wikihow.com/Play-Risk

    # Init Game
    # Place troops
    # Attack
    # Attack: NWTerr -> Alaska
    ###
    # TODO:
    config = {}
    with open('config.json') as f:
        config = json.load(f)
    Risk = Game(config)
    [Arthur, Bob, Charlie] = Risk.get_players()

    while not Risk.game_over():
        # Add optional loop for manually placing troops at beginning
        print(Risk.query_action())
        if Risk.turn.step == Step.Placement:
            placement_control(Risk)
        elif Risk.turn.step == Step.Attack:
            terr = input("Country to attack: ")

        # Risk.attack()


def placement_control(r):
    try:
        terr = input("Country to place: ")
        num = int(input("Number of troops: "))
        r.place(r.turn.curr, num, terr)
    except KeyError as e:
        print(e)
        placement_control(r)
    except ValueError as e:
        print(e)
        placement_control(r)


main()

from risk import Game
import json


def main():
    # Main control loop of Risk
    # https://www.alternatehistory.com/forum/threads/risk%C2%AE-maps.66855/

    # Init Game
    # Place troops
    # Attack
    # Attack: NWTerr -> Alaska
    ###
    config = {}
    with open('config.json') as f:
        config = json.load(f)
    g = Game(config)


main()

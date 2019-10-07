from risk import Game, Step
import json


def cli_gameplay():
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
    Risk.play()


if __name__ == "__main__":
    cli_gameplay()

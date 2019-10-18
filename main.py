from risk import Game, Step
import json
import argparse


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
    parser = argparse.ArgumentParser(
        description="Pick config file to run risk from")
    parser.add_argument('--file', help="Select config file to use",
                        default='./game_configs/config.json')
    args = parser.parse_args()
    config = {}
    with open(args.file) as f:
        config = json.load(f)
    Risk = Game(config)
    Risk.play()


if __name__ == "__main__":
    cli_gameplay()

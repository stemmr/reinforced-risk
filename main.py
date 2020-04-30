from game import Risk
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
    parser.add_argument("--file", help="Select config file to use",
                        default="./game_configs/config.json")
    parser.add_argument("--train", dest="training", action='store_true')
    parser.set_defaults(training=False)

    args = parser.parse_args()

    config = {}
    with open(args.file) as f:
        config = json.load(f)

    if not args.training:
        risk = Risk(config)
        risk.play()

    elif args.training:
        if config.players.type == "Human":
            raise Exception
        risk = Risk(config)
        for episode in range(100):
            risk.play()
            risk.reset()



if __name__ == "__main__":
    cli_gameplay()

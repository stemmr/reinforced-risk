from risk import Game


def main():
    # Main control loop of Risk
    # https://www.alternatehistory.com/forum/threads/risk%C2%AE-maps.66855/
    config = {
        "NAmerica": [
            "Alaska",
            "NWTerritory",
            "Alberta",
            "Ontario",
            "Quebec",
            "Greenland",
            "WUSA",
            "EUSA",
            "CAmerica"
        ],
        "SAmerica": [
            "Venezuela",
            "Peru",
            "Brazil",
            "Argentina"
        ],
        "Europe": [
            "Iceland",
            "GBritain",
            "Scandinavia",
            "NEurope",
            "WEurope",
            "SEurope",
            "Ukraine"
        ],
        "Africa": [
            "NAfrica",
            "Egypt",
            "Congo",
            "EAfrica",
            "Madagascar",
            "SAfrica"
        ],
        "Asia": [
            "Afghanistan",
            "MEast",
            "India",
            "Ural",
            "China",
            "Siberia",
            "Yakutsk",
            "Irkutsk",
            "Mongolia",
            "Siam",
            "Kamchatka",
            "Japan"
        ],
        "Australia": [
            "Indonesia",
            "NGuinea",
            "EAustralia",
            "WAustralia"
        ]

    }
    # Init Game
    # Place troops
    # Attack
    # Attack: NWTerr -> Alaska
    ###
    g = Game()

import json
import os


ABB_DIR = os.getcwd()
if "\\" in ABB_DIR:
    ABB_DIR = ABB_DIR+"\\"
else:
    ABB_DIR = ABB_DIR+"/"


def official_name(name, sport):
    """Return the official name of the specified team under our protocol.

    Uses the abbreviations json in the /abbreviations/ directory"""
    if "_" in sport:
        sport = sport.split("_")[1]
    with open(ABB_DIR + f"{sport}_naming.json", "r", encoding="utf-8") as file:
        names_json = json.load(file)
    # Remove weird characters like ";" that can sometimes appear on scoresandodds
    lower_name = name.replace(";", "").replace("'", "").lower()

    for key in names_json:
        if lower_name in [list_name.lower() for list_name in names_json[key]] + [key.lower()]:
            return key
    ### If it wasn't found it logs the error to the error list.
    print(f"Error running official_name(): Team '{name}' wasn't found in {ABB_DIR}{sport}_naming.json")

    return name

def get_abbreviation(name, sport):
    """This function extends the official_name() function, it uses it to find the abbreviation of the team that it receives."""
    team_official_name = official_name(name, sport)
    with open(ABB_DIR+f"{sport}_naming.json", "r", encoding="utf-8") as file:
        names_json = json.load(file)
    try:
        return names_json[team_official_name][0]
    except IndexError:
        print(f"Error running get_abbreviation(): Couldn't find an abbreviation for {team_official_name} on {sport}_naming.json")
    except KeyError:
        return team_official_name



s = get_abbreviation(name='miami-ohio', sport='nfl')
print(s)
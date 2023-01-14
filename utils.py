import json
import os


ABB_DIR = os.getcwd()
if "\\" in ABB_DIR:
    ABB_DIR = ABB_DIR+"\\"
else:
    ABB_DIR = ABB_DIR+"/"

def generate_id(date, away_team, home_team, game_number, sport):
    """This function generates a unique ID for a game, the format is 'YYYYMMDD-AWAYvsHOME-X', 
    X being the number of games played that day by those same teams against each other, 
    including the current one"""
    if "_" in sport:
        sport = sport.split("_")[1]
    return f"{date}-{get_abbreviation(away_team, sport)}vs{get_abbreviation(home_team, sport)}-{game_number}"

def official_name(name, sport):
    """Return the official name of the specified team under our protocol.
    
    Uses the abbreviations json in the /abbreviations/ directory"""
    if "_" in sport:
        sport = sport.split("_")[1]
    with open(ABB_DIR+f"{sport}_naming.json", "r", encoding="utf-8") as file:
        names_json = json.load(file)
    """Remove weird characters like ";" that can sometimes appear on scoresandodds"""
    lower_name = name.replace(";", "").replace("'", "").lower()

    for key in names_json:
        if lower_name in [list_name.lower() for list_name in names_json[key]] + [key.lower()]:
            return key
    ### If it wasn't found it logs the error to the error list.
    print(f"Error running official_name(): Team '{name}' wasn't found in {ABB_DIR}{sport}_naming.json")

    return name
#print(official_name("CWS", "mlb"))

def get_abbreviation(name, sport):
    """This function extends the official_name() function, it uses it to find the abbreviation of the team that it receives."""
    team_official_name = official_name(name, sport)
    with open(ABB_DIR+f"{sport}_naming.json", "r", encoding="utf-8") as file:
        names_json = json.load(file)
    try:
        return names_json[team_official_name][0]
    except IndexError:
        print(f"Error running get_abbreviation(): Couldn't find an abbreviation for {team_official_name} on {ABB_DIR}{sport}_naming.json")
    except KeyError:
        return team_official_name
#print(get_abbreviation("Chicago White Sox", "mlb"))


def short_official_name(name, sport):
    """This function will receive the name of a team from any source and return the official SHORT name of the team under our protocol"""
    with open(ABB_DIR+f"{sport}_naming.json", "r", encoding="utf-8") as file:
        names_json = json.load(file)

    #Remove weird characters like ";" that can sometimes appear on scoresandodds
    lower_name = name.replace(";", "").replace("'", "").lower()

    for key in names_json:
        possible_names = [list_name.lower() for list_name in names_json[key]] + [key.lower()]
        if lower_name in possible_names:
            try:
                return names_json[key][1]
            except IndexError:
                print(f"Error running short_official_name(): Short name for '{name}' wasn't found in {ABB_DIR}{sport}_naming.json")
    ### If it wasn't found it logs the error to the error list.
    print(f"Team '{name}' wasn't found in {ABB_DIR}{sport}_naming.json")

    return name
#print(short_official_name("BYU", "ncaaf"))

### Credits to Narnie from stackoverflow on this one
def trueround(number, places=0):
    '''
    trueround(number, places)

    example:

        >>> trueround(2.55, 1) == 2.6
        True

    uses standard functions with no import to give "normal" behavior to 
    rounding so that trueround(2.5) == 3, trueround(3.5) == 4, 
    trueround(4.5) == 5, etc. Use with caution, however. This still has 
    the same problem with floating point math. The return object will 
    be type int if places=0 or a float if places=>1.

    number is the floating point number needed rounding

    places is the number of decimal places to round to with '0' as the
        default which will actually return our interger. Otherwise, a
        floating point will be returned to the given decimal place.

    Note:   Use trueround_precision() if true precision with
            floats is needed

    GPL 2.0
    copywrite by Narnie Harshoe <signupnarnie@gmail.com>
    '''
    #if number in [NaN, Inf]:
        #return number
    place = 10**(places)
    rounded = (int(number*place + 0.5 if number>=0 else -0.5))/place
    if rounded == int(rounded):
        rounded = int(rounded)
    return rounded

"""Month translation format"""

def month_number(name):
    """Return the official name of the specified team under our protocol.

    Uses the abbreviations json in the /abbreviations/ directory"""
    #if "_" in sport:
        #sport = sport.split("_")[1]
    with open("months.json", "r", encoding="utf-8") as file:
        names_json = json.load(file)
    #"""Remove weird characters like ";" that can sometimes appear on scoresandodds"""
    month_number = name.replace(";", "").replace("'", "").lower()

    for key in names_json:
        if month_number in [list_name.lower() for list_name in names_json[key]] + [key.lower()]:
            return key
    ### If it wasn't found it logs the error to the error list.
    print(f"Error running official_name(): Team '{name}' wasn't found in {ABB_DIR}{sport}_naming.json")

    return name



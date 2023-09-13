import re
import sys
import requests

API_TOKEN = "5046455350ed4dab870f83580522cea0"
BASE_URL = "https://api.football-data.org/v4/competitions/"
HEADERS = {"X-AUTH-TOKEN": API_TOKEN}

league_ids = {
    "Bundesliga": "BL1",
    "Eredivisie": "DED",
    "Campeonato Brasileiro Série A": "BSA",
    "Primera Division": "PD",
    "Ligue 1": "FL1",
    "Championship": "ELC",
    "Primeira Liga": "PPL",
    "Serie A": "SA",
    "Premier League": "PL",
}
# length is max matchday
league_length = {
    "BL1": 34,
    "DED": 34,
    "BSA": 38,
    "PD": 38,
    "FL1": 34,
    "ELC": 46,
    "PPL": 34,
    "SA": 38,
    "PL": 38,
}


class League:
    def __init__(self, id):
        self.id = id

    def get():
        while True:
            s = input("What league? ").title().strip()
            if s in league_ids:
                id = league_ids[s]
                return id
            else:
                print("Invalid league")


class Fixtures(League):
    def __init__(self, num, id):
        super().__init__(id)
        self.num = num

    def matchday(id):
        while True:
            n = input(f"What matchday? ")
            if match := re.search(r"^([0-9][0-9]?)$", n):
                if int(match.group(1)) > league_length[id] or int(match.group(1)) == 0:
                    print("Invalid matchday")
                else:
                    return match.group(1)
            else:
                print("Invalid matchday")

    def operate(self):
        print(f"{'Home':<30}{'  ':<5}{'Away':<30}{'Time':<15}{'Date':<10}")
        response = requests.get(
            f"{BASE_URL}{self.id}/matches?matchday={self.num}", headers=HEADERS
        )
        o = response.json()
        schedule = []
        for match in o["matches"]:
            _match = re.search(
                r"([0-9]{4})-([0-9]{2})-([0-9]{2})T([0-9]{2})(:[0-9]{2}):[0-9]{2}Z",
                match["utcDate"],
            )
            new_time = f"{int(_match.group(4)) + 1}{_match.group(5)} BST"
            new_date = f"{_match.group(3)}-{_match.group(2)}-{_match.group(1)}"
            schedule.append(
                f"{match['homeTeam']['name']:<30}{'vs':<5}{match['awayTeam']['name']:<30}{new_time:<15}{new_date:<10}"
            )
        for match in schedule:
            print(match)


class Table(League):
    def __init__(self, id):
        super().__init__(id)

    def operate(self):
        print(f"{'Position':<10}{'Team':<30}{'Record (W/D/L)':<20}{'Points':<10}")
        response = requests.get(f"{BASE_URL}{self.id}/standings", headers=HEADERS)
        o = response.json()
        standings = []
        for team in o["standings"][0]["table"]:
            record = f"{team['won']}-{team['draw']}-{team['lost']}"
            standings.append(
                f"{team['position']:<10}{team['team']['name']:<30}{record:<20}{team['points']:<10}"
            )
        for standing in standings:
            print(standing)


class Scorers(League):
    def __init__(self, id):
        super().__init__(id)

    def operate(self):
        print(f"{'Position':<12}{'Name':<30}{'Team':<30}{'Goals':<10}")
        response = requests.get(f"{BASE_URL}{self.id}/scorers", headers=HEADERS)
        o = response.json()
        scorers = []
        n = 0
        for person in o["scorers"]:
            n += 1
            scorers.append(
                f"{n:<12}{person['player']['name']:<30}{person['team']['name']:<30}{person['goals']:<10}"
            )
        for player in scorers:
            print(player)


def main():
    function = task()
    if function == "fixtures":
        id = League.get()
        n = Fixtures.matchday(id)
        Fixtures(n, id).operate()

    elif function == "scorers":
        id = League.get()
        Scorers(id).operate()

    elif function == "table":
        id = League.get()
        Table(id).operate()


def task():
    s = input(f"Table, fixtures or top scorers? ")
    if re.search(r"[\W]?fixtures?[\W]?", s, re.IGNORECASE):
        return f"fixtures"

    elif re.search(r"[\W]?tables?[\W]?", s, re.IGNORECASE):
        return f"table"

    elif re.search(r"[\W]?top[\W]?.+[\W]?scorers?[\W]?", s, re.IGNORECASE):
        return f"scorers"

    else:
        sys.exit("Desired task is unavailable")


if __name__ == "__main__":
    main()

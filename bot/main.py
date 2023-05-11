from requests import get
import socketio
import json
from pprint import pprint as pp

sio = socketio.Client()
sio.connect("https://apirads.peekoe.net")

PUBLICS = [''.join(sorted(x)) for x in ["AA", "AD", "AS", "DA", "DD", "DS", "SA", "SD", "SS"]]
HANDS = [
    ''.join(sorted(x))
    for x in [
        "AAAA",
        "AAAD",
        "AAAS",
        "AADD",
        "AADS",
        "AASS",
        "ADDD",
        "ADDS",
        "ADSS",
        "ASSS",
        "DDDD",
        "DDDS",
        "DDSS",
        "DSSS",
        "SSSS",
    ]
]

# first key is the move the bot makes, second key is the move the opponent makes
# winrate = dict([((x, y), 0.0) for x in MOVES for y in MOVES])
winrate = dict([(x, dict([(y, 0.5) for y in HANDS])) for x in PUBLICS])
most_recent_publics = {}
most_recent_results = {}
last_response = {}


def get_public():
    global most_recent_publics
    most_recent_publics = get("https://apirads.peekoe.net/dump").json()
    # sort all of the keys and put them back in dict
    most_recent_publics = dict(
        [(x, ''.join(sorted(most_recent_publics[x]))) for x in most_recent_publics]
    )


@sio.on("json")  # type:ignore
def receive_results(data):
    global most_recent_results
    most_recent_results = data


@sio.on("NEXT")  # type:ignore
def next(data):
    global most_recent_publics, most_recent_results, last_response, winrate
    get_public()
    update_winrate()
    sio.emit("json", json.dumps(make_move()))


def update_winrate():
    global most_recent_publics, most_recent_results, last_response, winrate
    for player in most_recent_results:
        player_pub = most_recent_publics[player]
        # print(last_response)
        print(player_pub)
        print(last_response["public"])
        calc_hand = ''.join(sorted(last_response["public"] + last_response[player_pub]))

        if most_recent_results[player]["BOT"] >= 0:
            winrate[player_pub][calc_hand] = (winrate[player_pub][calc_hand] + 1) / 2
        else:
            winrate[player_pub][calc_hand] = (winrate[player_pub][calc_hand] - 1) / 2

    # pp(winrate)


def make_move():
    global most_recent_publics, most_recent_results, last_response, winrate
    cans = dict([(x, 0) for x in PUBLICS])
    pubsToMoves = {}

    for player, public in most_recent_publics.items():
        match = winrate[public]

        for move, rate in match.items():
            if rate > match[move]:
                pubsToMoves[player] = move

        for move in pubsToMoves.values():
            for can in cans:
                if can in moves:
                    cans[can] += 1

    bestPub = sorted(cans.items(), key=lambda x: x[1])[0][0]
    response = {}
    response["public"] = bestPub

    # pp(pubsToMoves)
    for pub, hand in pubsToMoves.items():
        if bestPub in hand:
            response[pub] = hand.replace(bestPub, "")
        else:
            response[pub] = bestPub

    for not_set in set(response.keys()).difference(set(PUBLICS)):
        response[not_set] = bestPub

    response["username"] = "BOT"
    last_response = response
    pp(response)

    return response


if __name__ == "__main__":
    last_response = json.dumps(
            {
                "username": "BOT",
                "public": "DD",
                "AA": "DD",
                "AD": "DD",
                "AS": "DD",
                "DA": "DD",
                "DD": "DD",
                "DS": "DD",
                "SA": "DD",
                "SD": "SD",
                "SS": "SS",
            }
        )

    sio.emit("json", last_response)

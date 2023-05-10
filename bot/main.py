from requests import get
import socketio

sio = socketio.Client()
sio.connect("ws://apirad.peekoe.net")

MOVES = ["AA", "AD", "AS", "DA", "DD", "DS", "SA", "SD", "SS"]

# first key is the move the bot makes, second key is the move the opponent makes
winrate = dict([((x, y), 0.0) for x in MOVES for y in MOVES])
most_recent_publics = {}
most_recent_results = {}


def get_public():
    most_recent_results = get("http://apirad.peekoe.net/public").json()


@sio.on("json")  # type:ignore
def receive_results(data):
    most_recent_results = data


@sio.on("NEXT")  # type:ignore
def next():
    get_public()
    update_winrate(most_recent_results, most_recent_publics)
    sio.emit("message", make_move())


def update_winrate(results, player_publics):
    for player, result in results.items():
        choice = player_publics[player]

        if result == "1":
            winrate[choice] = max((winrate[choice] + 1) / 2, 1)

        if result == "-1":
            winrate[player] = min((winrate[choice] - 1) / 2, 0)


def make_move():
    response = {}

    for bot_move, player_move in winrate:
        if bot_move not in response:
            response[bot_move] = player_move
            continue

        if winrate[bot_move, player_move] > winrate[bot_move, response[bot_move]]:
            response[bot_move] = player_move

    return response

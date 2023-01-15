from flask import Flask, Response, render_template
from typing import Dict
import threading
import uuid
import json

import GameEngine


class EndpointAction(object):

    def __init__(self, action):
        self.action = action
        self.response = Response(status=200, headers={})

    def __call__(self, *args, **kwargs):
        print(args)
        print(kwargs)
        return self.action(*args, **kwargs)


class GameHandler(object):
    app = None

    def __init__(self, name):
        self.config = json.loads(open('settings.json').read())
        self.app = Flask(name)
        self.add_endpoints()
        threading.Thread(target=self.run_api, args=()).start()

        self.games: Dict[str, GameEngine.Game] = {}

        players = [GameEngine.Player(player_name=f"player_{x}", player_id=str(uuid.uuid4())) for x in range(5)]
        self.crate_game(name="test game", players=players, config=self.config)

        for game in self.games:
            print(self.games[game].info())

    def crate_game(self, name: str, players: list[GameEngine.Player], config: dict):
        game_id = str(uuid.uuid4())
        self.games[game_id] = GameEngine.Game(11, 11, name, game_id, players, config)

    def add_endpoints(self):
        self.add_endpoint(endpoint='/', endpoint_name='index', handler=self.index)
        self.add_endpoint(endpoint='/game/<game_id>', endpoint_name='game', handler=self.game)

    def run_api(self):
        self.app.run(host=self.config["host"], port=self.config["port"], debug=self.config["debug"])

    def add_endpoint(self, endpoint=None, endpoint_name=None, handler=None):
        self.app.add_url_rule(endpoint, endpoint_name, EndpointAction(handler))

    def index(self):
        return render_template('index.html')

    def game(self, game_id):
        if not game_id in self.games:
            return render_template("game_not_found.html")
        game = self.games[game_id]
        return render_template("game.html", game=game)


if __name__ == "__main__":
    app = GameHandler('game')


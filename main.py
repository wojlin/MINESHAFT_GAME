from flask import Flask, Response, render_template, request
from typing import Dict
import threading
import uuid
import json
import sys
import ast
import os

import GameEngine
import Cards

class EndpointAction(object):

    def __init__(self, action):
        self.action = action
        self.response = Response(status=200, headers={})

    def __call__(self, *args, **kwargs):
        data = dict(request.args)
        return self.action(data)


class GameHandler(object):
    app = None

    def __init__(self, name):
        self.config = json.loads(open('settings.json').read())
        self.app = Flask(name)
        self.add_endpoints()
        threading.Thread(target=self.run_api, args=()).start()

        self.games: Dict[str, GameEngine.Game] = {}
        players: Dict[str, GameEngine.Player] = {}

        for x in range(5):
            new_id = str(uuid.uuid4())
            players[new_id] = GameEngine.Player(player_name=f"player_{x}", player_id=new_id)

        self.crate_game(name="test game", players=players, config=self.config)

        for game in self.games:
            print(self.games[game].info())

    def crate_game(self, name: str, players: Dict[str, GameEngine.Player], config: dict):
        game_id = str(uuid.uuid4())
        self.games[game_id] = GameEngine.Game(name, game_id, players, config)

    def add_endpoints(self):
        self.add_endpoint(endpoint='/', endpoint_name='index', handler=self.index)
        self.add_endpoint(endpoint='/game', endpoint_name='game', handler=self.game)
        self.add_endpoint(endpoint='/game/end_turn', endpoint_name='end turn', handler=self.end_turn)
        self.add_endpoint(endpoint='/game/fetch_game_status', endpoint_name='fetch game status', handler=self.fetch_game_status)
        self.add_endpoint(endpoint='/game/is_move_correct', endpoint_name='is move correct', handler=self.is_move_correct)

    def run_api(self):
        self.app.run(host=self.config["host"], port=self.config["port"], debug=self.config["debug"])

    def add_endpoint(self, endpoint=None, endpoint_name=None, handler=None):
        self.app.add_url_rule(endpoint, endpoint_name, EndpointAction(handler))

    def index(self):
        return render_template('index.html')

    def game(self, data: dict):
        if "game_id" not in data or "player_id" not in data:
            return render_template("404.html")

        if data["game_id"] not in self.games:
            return render_template("game_not_found.html")

        game = self.games[data["game_id"]]

        if data["player_id"] not in game.players:
            return render_template("player_not_found.html")

        return render_template("game.html", game=game, player_id=data["player_id"])

    def __build_card_from_json(self, data):
        if data["card_type"] == "Tunnel Card":
            way_top = data["card_directions"]["way_top"]
            way_right = data["card_directions"]["way_right"]
            way_bottom = data["card_directions"]["way_bottom"]
            way_left = data["card_directions"]["way_left"]
            destructible = data["destructible"]
            overwrite = data["overwrite"]
            card_id = data["card_id"]
            return Cards.TunnelCard(way_top=way_top,
                                    way_right=way_right,
                                    way_bottom=way_bottom,
                                    way_left=way_left,
                                    destructible=destructible,
                                    overwrite=overwrite,
                                    empty=False,
                                    card_id=card_id)

        elif data["card_type"] == "Action Card":
            action_type = data["action_type"]
            is_positive_effect = data["is_positive_effect"]
            card_id = data["card_id"]
            return Cards.ActionCard(action_type=action_type,is_positive_effect=is_positive_effect,card_id=card_id)
        raise Exception("incorrect card type")

    def end_turn(self, data: dict):
        if "game_id" not in data:
            return {"message_type": "error", "message": "game parameters not exist in request"}
        if "player_id" not in data:
            return {"message_type": "error", "message": "player parameters not exist in request"}
        if "player_move" not in data:
            return {"message_type": "error", "message": "player move parameters not exist in request"}
        if data["game_id"] not in self.games:
            return {"message_type": "error", "message": "game not found"}

        game = self.games[data["game_id"]]

        if data["player_id"] not in game.players:
            return {"message_type": "error", "message": "player not found"}

        if data["player_id"] != game.turn:
            return {"message_type": "error", "message": f"you cannot end turn. it's {game.turn} turn"}

        player = game.players[data["player_id"]]

        data["player_move"] = json.loads(data["player_move"])
        data["player_move"]['card'] = json.loads(data["player_move"]['card'])
        card = self.__build_card_from_json(data["player_move"]["card"])

        card_exist = False
        for player_card in player.player_cards:
            if player_card.is_card_the_same(card):
                card_exist = True

        if card_exist is False:
            return {"message_type": "error", "message": f"you dont have card that you used in your inventory"}


        if data["player_move"]["move_type"] == "trash":
            for i in range(len(player.player_cards)):
                if player.player_cards[i].is_card_the_same(card):
                    player.player_cards.pop(i)
                    break
        elif card.card_type == card.TUNNEL_TYPE:
            pos_x = int(data["player_move"]["move_pos"]["x"])
            pos_y = int(data["player_move"]["move_pos"]["y"])
            status = game.check_game_tunnel_card_rules(card, pos_x=pos_x, pos_y=pos_y)
            if status is False:
                return {"message_type": "error", "message": f"move is not valid"}
            game.board[pos_y][pos_x] = card
        elif card.card_type == card.ACTION_TYPE:
            # TODO: check game action card rules
            return {"message_type": "error", "message": f"not implemented yet"}
        else:
            raise Exception("incorrect card type")

        game.give_card_from_stack(data["player_id"])

        print(game.end_turn())

        return {"message_type": "info", "message": f"you ended turn!"}

    def is_move_correct(self, data):
        try:
            if "game_id" not in data or "player_id" not in data:
                return {"message_type": "error", "message": "game parameters not exist in request"}

            if "player_id" not in data:
                return {"message_type": "error", "message": "player parameters not exist in request"}

            if "card" not in data:
                return {"message_type": "error", "message": "no tunnel card specified"}

            if data["game_id"] not in self.games:
                return {"message_type": "error", "message": "game not found"}

            game = self.games[data["game_id"]]

            if data["player_id"] not in game.players:
                return {"message_type": "error", "message": "player not found"}

            print(data["card"])
            card_info = json.loads(data["card"])

            if card_info["card_type"] != "Tunnel Card" and card_info["card_type"] != "Action Card":
                return {"message_type": "error", "message": "wrong card type"}

            way_top = card_info["card_directions"]["way_top"]
            way_right = card_info["card_directions"]["way_right"]
            way_bottom = card_info["card_directions"]["way_bottom"]
            way_left = card_info["card_directions"]["way_left"]
            destructible = card_info["destructible"]
            overwrite = card_info["overwrite"]
            pos_x = int(data["pos_x"])
            pos_y = int(data["pos_y"])

            card = Cards.TunnelCard(way_top=way_top,
                                    way_right=way_right,
                                    way_bottom=way_bottom,
                                    way_left=way_left,
                                    destructible=destructible,
                                    overwrite=overwrite,
                                    empty=False)

            isValidMove = game.check_game_tunnel_card_rules(card=card, pos_x=pos_x, pos_y=pos_y)

            if isValidMove:
                return {"message_type": "game_status_data", "message": True}
            else:
                return {"message_type": "game_status_data", "message": False}

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            error = f"{exc_type}\n{fname}\n{exc_tb.tb_lineno}"
            return {"message_type": "error", "message": f"unexpected error: {error}"}

    def fetch_game_status(self, data):
        if "game_id" not in data:
            return {"message_type": "error", "message": "game parameters not exist in request"}

        if "player_id" not in data:
            return {"message_type": "error", "message": "player parameters not exist in request"}

        if data["game_id"] not in self.games:
            return {"message_type": "error", "message": "game not found"}

        game = self.games[data["game_id"]]

        if data["player_id"] not in game.players:
            return {"message_type": "error", "message": "player not found"}

        players_actions = {}
        for player_id, player_obj in game.players.items():
            players_actions[player_id] = player_obj.player_actions

        player_cards = {f"{card.picture_url}": card.card_info for card in game.players[data["player_id"]].player_cards}

        return {"message_type": "game_status_data",
                "game_turn": game.turn,
                "cards_left": len(game.cards),
                "game_round": game.round,
                "players_actions": players_actions,
                "board": [[game.board[y][x].picture_url for x in range(game.BOARD_SIZE_X)] for y in range(game.BOARD_SIZE_Y)],
                "player_cards": player_cards}


if __name__ == "__main__":
    app = GameHandler('game')


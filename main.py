import copy
import logging
from flask import Flask, Response, render_template, request
from typing import Dict
import threading
import uuid
import json
import sys
import ast
import os

import GameEngine
from GameRoom import GameRoom
import Cards

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

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
        self.game_name = "TUNNEL GAME"
        self.config = json.loads(open('settings.json').read())
        self.app = Flask(name)
        self.add_endpoints()
        threading.Thread(target=self.run_api, args=()).start()

        self.games: Dict[str, GameEngine.Game] = {}
        self.rooms: Dict[str, GameRoom] = {}

        if self.config["development_stage"]:
            players: Dict[str, GameEngine.Player] = {}

            for x in range(3):
                room_id = str(uuid.uuid4())
                self.rooms[room_id] = GameRoom(room_comment="test comment",
                                               room_name=f'room {x}',
                                               room_id=room_id,
                                               game_host_player_id=str(uuid.uuid4()),
                                               game_host_player_name='host',
                                               room_password="1234" if x % 3 == 0 else '',
                                               config=self.config)

            for x in range(5):
                new_id = str(uuid.uuid4())
                players[new_id] = GameEngine.Player(player_name=f"player_{x}", player_id=new_id)

            self.__crate_game(name="test game", players=players, config=self.config)

            for game in self.games:
                print(self.games[game].info())
                with open("path.txt", 'w') as file:
                    file.write(self.games[game].pathfinding_grid_info())

            for room in self.rooms:
                print(self.rooms[room].info())

    def room(self, data):
        if "player_id" not in data:
            return {"message_type": "error", "message": "player id not in request data"}

        if "room_id" not in data:
            return {"message_type": "error", "message": "room id not in request data"}

        if data["room_id"] not in self.rooms:
            return {"message_type": "error", "message": "room does not exist"}

        if data["player_id"] not in self.rooms[data["room_id"]].players:
            return {"message_type": "error", "message": "room does not exist"}

        return render_template("room.html", room=self.rooms[data["room_id"]], player_id=data["player_id"], game_name=self.game_name)

    def join_room(self, data):
        if "player_name" not in data:
            return {"message_type": "error", "message": "player name not in request data"}

        if "room_id" not in data:
            return {"message_type": "error", "message": "room id not in request data"}

        if "room_password" not in data:
            return {"message_type": "error", "message": "room password not in request data"}

        room_id = data["room_id"]
        room = self.rooms[room_id]

        if room.locked:
            if data["room_password"] != room.room_password:
                return {"message_type": "error", "message": "invalid password!"}

        if room.players_amount > 10:
            return {"message_type": "error", "message": "room full!"}

        player_id = str(uuid.uuid4())
        room.add_player_to_room(player_id, data["player_name"])

        return {"message_type": "status",
                "message": "joined room!",
                "data": {
                    "room_id": room_id,
                    "player_id": player_id
                }
                }

    def create_room(self, data):
        if "player_name" not in data:
            return {"message_type": "error", "message": "player name not in request data"}

        if "room_name" not in data:
            return {"message_type": "error", "message": "room name not in request data"}

        if "room_comment" not in data:
            return {"message_type": "error", "message": "room comment not in request data"}

        if "room_password" not in data:
            return {"message_type": "error", "message": "room password not in request data"}

        room_id = str(uuid.uuid4())
        player_id = str(uuid.uuid4())
        player_name = data["player_name"]
        room_name = data["room_name"]
        room_password = data["room_password"]
        room_comment = data["room_comment"]
        room = GameRoom(room_comment=room_comment,
                        room_name=room_name,
                        room_id=room_id,
                        game_host_player_id=player_id,
                        game_host_player_name=player_name,
                        room_password=room_password,
                        config=self.config)

        self.rooms[room_id] = room
        return {"message_type": "status",
                "message": "game room created!",
                "data": {
                    "room_id": room_id,
                    "player_id": player_id
                        }
                }

    def fetch_rooms_status(self, data):
        rooms_status = {}
        for roomid in self.rooms:
            room = self.rooms[roomid]
            rooms_status[room.room_id] = room.fetch_status()

        return {"message_type": "status", "data": rooms_status}

    def fetch_room_status(self, data):

        if "room_id" not in data:
            return {"message_type": "error", "message": "room id not in request data"}

        if data["room_id"] not in self.rooms:
            return render_template("room_not_found.html")

        room = self.rooms[data["room_id"]]

        status = room.fetch_status()

        return {"message_type": "status", "data": status}

    def start_game(self, data):

        if "room_id" not in data:
            return {"message_type": "error", "message": "room id not in request data"}

        if "player_id" not in data:
            return {"message_type": "error", "message": "player id not in request data"}

        if data["room_id"] not in self.rooms:
            return render_template("room_not_found.html")

        room = self.rooms[data["room_id"]]

        if data["player_id"] != room.host_id:
            return {"message_type": "error", "message": "only host can start the game"}

        room.game_started = True
        room.status = "in game"
        self.games[room.room_id] = GameEngine.Game(game_id=room.room_id,
                                              config=self.config,
                                              name=room.room_name,
                                              players=copy.deepcopy(room.players))

        status = room.fetch_status()

        return {"message_type": "status", "data": status}

    def __crate_game(self, name: str, players: Dict[str, GameEngine.Player], config: dict):
        game_id = str(uuid.uuid4())
        self.games[game_id] = GameEngine.Game(name, game_id, players, config)

    def add_endpoints(self):
        self.add_endpoint(endpoint='/', endpoint_name='index', handler=self.index)
        self.add_endpoint(endpoint='/create_room', endpoint_name='create room', handler=self.create_room)
        self.add_endpoint(endpoint='/join_room', endpoint_name='join room', handler=self.join_room)
        self.add_endpoint(endpoint='/fetch_rooms_status', endpoint_name='fetch rooms status', handler=self.fetch_rooms_status)
        self.add_endpoint(endpoint='/room', endpoint_name='room', handler=self.room)
        self.add_endpoint(endpoint='/room/fetch_room_status', endpoint_name='fetch room status', handler=self.fetch_room_status)
        self.add_endpoint(endpoint='/room/start_game', endpoint_name='start game', handler=self.start_game)
        self.add_endpoint(endpoint='/game', endpoint_name='game', handler=self.game)
        self.add_endpoint(endpoint='/game/end_turn', endpoint_name='end turn', handler=self.end_turn)
        self.add_endpoint(endpoint='/game/fetch_game_status', endpoint_name='fetch game status', handler=self.fetch_game_status)
        self.add_endpoint(endpoint='/game/is_move_correct', endpoint_name='is move correct', handler=self.is_move_correct)

    def run_api(self):
        self.app.run(host=self.config["host"], port=self.config["port"], debug=self.config["debug"])

    def add_endpoint(self, endpoint=None, endpoint_name=None, handler=None):
        self.app.add_url_rule(endpoint, endpoint_name, EndpointAction(handler))

    def index(self, *args, **kwargs):
        return render_template('index.html', rooms=self.rooms)

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
            empty = data["empty"]
            card_id = data["card_id"]
            return Cards.TunnelCard(way_top=way_top,
                                    way_right=way_right,
                                    way_bottom=way_bottom,
                                    way_left=way_left,
                                    destructible=destructible,
                                    overwrite=overwrite,
                                    empty=empty,
                                    card_id=card_id)

        elif data["card_type"] == "Action Card":
            action_type = data["action_type"]
            is_positive_effect = data["is_positive_effect"]
            card_id = data["card_id"]
            return Cards.ActionCard(action_type=action_type,is_positive_effect=is_positive_effect,card_id=card_id)
        raise Exception("incorrect card type")


    def end_turn(self, data: dict):
        print("ending turn...")

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
            self.games[data["game_id"]].give_card_from_stack(data["player_id"], card.card_id)
        elif data["player_move"]["move_type"] == "map":
            pos_x = int(data["player_move"]["move_pos"]["x"])
            pos_y = int(data["player_move"]["move_pos"]["y"])
            status = game.check_game_tunnel_card_rules(card, pos_x=pos_x, pos_y=pos_y)
            if status is False:
                return {"message_type": "error", "message": f"move is not valid"}
            game.board[pos_y][pos_x] = copy.deepcopy(card)
            game.update_pathfinding_grid(pos_x, pos_y, card)
            with open('path.txt', 'w') as file:
                file.write(game.pathfinding_grid_info())
            self.games[data["game_id"]].give_card_from_stack(data["player_id"], card.card_id)
        elif data["player_move"]["move_type"] == "action":
            des_player_id = data["player_move"]["move_action"]['desired_player_id']
            des_player_action = int(data["player_move"]["move_action"]['desired_player_action'])
            if des_player_id not in game.players:
                return {"message_type": "error", "message": "player not found!"}
            des_player = game.players[des_player_id]
            if int(des_player_action) != int(card.action_type):
                return {"message_type": "error", "message": f"move is not valid"}
            if des_player.player_actions[des_player_action] == card.is_positive_effect:
                return {"message_type": "error", "message": f"move is not valid"}
            des_player.player_actions[des_player_action] = card.is_positive_effect
            self.games[data["game_id"]].give_card_from_stack(data["player_id"], card.card_id)
        else:
            raise Exception("incorrect card type")

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

            player = game.players[data['player_id']]

            #print(data)
            card_info = json.loads(data["card"])

            if card_info["card_type"] != "Tunnel Card" and card_info["card_type"] != "Action Card":
                return {"message_type": "error", "message": "wrong card type"}

            if card_info["card_type"] == "Action Card":
                if 'desired_player_id' not in data or 'desired_player_action' not in data:
                    return {"message_type": "game_status_data", "message": False}
                else:
                    des_player_id = data['desired_player_id']
                    des_player_action = int(data['desired_player_action'])
                    if des_player_id not in game.players:
                        return {"message_type": "error", "message": "player not found!"}
                    des_player = game.players[des_player_id]
                    if des_player_action != int(card_info['action_type']):
                        return {"message_type": "game_status_data", "message": False}
                    if des_player.player_actions[des_player_action] == card_info['is_positive_effect']:
                        return {"message_type": "game_status_data", "message": False}

                    return {"message_type": "game_status_data", "message": True}
            elif card_info["card_type"] == "Tunnel Card":
                if 'pos_x' not in data or 'pos_y' not in data:
                    return {"message_type": "game_status_data", "message": False}
                if not all(player.player_actions):
                    return {"message_type": "game_status_data", "message": False}

                way_top = card_info["card_directions"]["way_top"]
                way_right = card_info["card_directions"]["way_right"]
                way_bottom = card_info["card_directions"]["way_bottom"]
                way_left = card_info["card_directions"]["way_left"]
                empty = card_info["empty"]
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
                                        empty=empty)

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
        #print("fetching status...")
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

        cards = game.players[data["player_id"]].player_cards

        player_cards = {f"slot_{cards.index(card)}": card.card_info for card in cards}

        return {"message_type": "game_status_data",
                "game_turn": game.turn,
                "cards_left": len(game.cards),
                "game_round": game.round,
                "players_actions": players_actions,
                "board": [[game.board[y][x].picture_url for x in range(game.BOARD_SIZE_X)] for y in range(game.BOARD_SIZE_Y)],
                "player_cards": player_cards}


if __name__ == "__main__":
    app = GameHandler('game')


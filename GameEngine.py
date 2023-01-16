from typing import Dict
import random
import math

from Cards import Card
from Player import Player

class GameEngine:
    def __init__(self, cells_x: int, cells_y: int, name: str, game_id: str, players: Dict[str, Player], config: dict):
        self.board_size_x = cells_x
        self.board_size_y = cells_y
        self.name = name
        self.game_id = game_id
        self.players = players
        self.config = config

    def check_game_creation_rules(self):
        if len(self.players) < 3:
            return {"message_type": "error", "message_content": "not enough players"}
        elif len(self.players) > 10:
            return {"message_type": "error", "message_content": "too much players"}
        else:
            return {"message_type": "status", "message_content": "game can be created"}

    def info(self):
        info_str =  f"uuid: {self.game_id}\n" \
                    f"name: {self.name}\n" \
                    f"players:\n[\n"

        for player in self.players:
            player = self.players[player]
            url_base = f"http://{self.config['host']}:{self.config['port']}/game"
            url_args = f"?game_id={self.game_id}&player_id={player.player_id}"

            info_str += f"name: {player.player_name}     id: {player.player_id}     url: {url_base+url_args}\n"

        info_str += "]\n"

        info_str += f"board size: {self.board_size_x}x{self.board_size_y}\n"
        return info_str


class Game(GameEngine):
    def __init__(self, cells_x: int, cells_y: int, name: str, game_id: str, players: Dict[str, Player], config: dict):
        GameEngine.__init__(self,
                            cells_x=cells_x,
                            cells_y=cells_y,
                            name=name,
                            game_id=game_id,
                            players=players,
                            config=config)

        self.__current_turn_num = 0
        self.turn = list(self.players.values())[self.__current_turn_num].player_id

        self.good_player = "Solider"
        self.bad_player = "Saboteur"

        for player_id, player_obj in players.items():
            player_obj.player_role = self.good_player

        self.saboteur_amount = math.floor((len(self.players) - 1) / 2)

        for x in range(self.saboteur_amount):
            player_id, player_obj = random.choice(list(self.players.items()))
            player_obj.player_role = self.bad_player

    def end_turn(self):
        self.__current_turn_num = self.__current_turn_num + 1 if self.__current_turn_num < len(self.players) else 0
        self.turn = list(self.players.values())[self.__current_turn_num].player_id
        return f"turn ended, now its '{self.players[self.turn].player_name}' turn"



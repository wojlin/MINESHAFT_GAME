from Cards import Card
from Player import Player
class GameEngine:
    def __init__(self, cells_x: int, cells_y: int, name: str, game_id: str, players: list[Player], config: dict):
        self.board_size_x = cells_x
        self.board_size_y = cells_y
        self.name = name
        self.game_id = game_id
        self.players = players
        self.config = config

    def info(self):
        info_str =  f"uuid: {self.game_id}\n" \
                    f"name: {self.name}\n" \
                    f"players:\n[\n"

        for player in self.players:
            info_str += f"name: {player.player_name}     id: {player.player_id}\n"

        info_str += "]\n"

        info_str += f"board size: {self.board_size_x}x{self.board_size_y}\n"
        info_str += f"game url: http://{self.config['host']}:{self.config['port']}/game/{self.game_id}"
        return info_str


class Game(GameEngine):
    def __init__(self, cells_x: int, cells_y: int, name: str, game_id: str, players: list[Player], config: dict):
        GameEngine.__init__(self,
                            cells_x=cells_x,
                            cells_y=cells_y,
                            name=name,
                            game_id=game_id,
                            players=players,
                            config=config)



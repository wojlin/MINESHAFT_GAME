from Player import Player


class GameRoom:
    def __init__(self,
                 room_comment: str,
                 room_name: str,
                 room_id: str,
                 game_host_player_id: str,
                 game_host_player_name: str,
                 room_password: str,
                 config: dict):

        self.config = config
        self.room_comment = room_comment
        self.room_name = room_name
        self.room_id = room_id
        self.room_password = room_password
        self.locked = True if self.room_password else False
        self.players_amount = 1
        self.host_id = game_host_player_id
        self.players = {game_host_player_id: Player(game_host_player_name, game_host_player_id)}

    def add_player_to_room(self, player_id: str, player_name: str):
        self.players[player_id] = Player(player_name, player_id)
        self.players_amount += 1

    def info(self):
        info_str = f"room: {self.room_name}  "
        url_base = f"http://{self.config['host']}:{self.config['port']}/room"
        url_args = f"?room_id={self.room_id}&player_id={list(self.players.values())[0].player_id}"
        info_str += url_base+url_args
        return info_str

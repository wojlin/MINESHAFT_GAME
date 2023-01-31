from Player import Player


class GameRoom:
    def __init__(self, room_id: str, game_host_player_id: str):
        self.room_id = room_id
        self.players = {game_host_player_id: game_host_player_id}

    def add_player_to_room(self, player_id: str):
        self.players[player_id] = player_id

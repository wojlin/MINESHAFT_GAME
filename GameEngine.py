from Cards import Card

class GameEngine:
    def __init__(self, cells_x: int, cells_y: int, name: str, game_id: str):
        self.board_size_x = cells_x
        self.board_size_y = cells_y
        self.name = name
        self.game_id = game_id


class Game(GameEngine):
    def __init__(self, cells_x: int, cells_y: int, name: str, game_id: str):
        GameEngine.__init__(self, cells_x=cells_x, cells_y=cells_y, name=name, game_id=game_id)

    def info(self):
        return f"uuid: {self.game_id}\n" \
               f"name: {self.name}\n" \
               f"board size: {self.board_size_x}x{self.board_size_y}\n"

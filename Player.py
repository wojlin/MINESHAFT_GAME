class Player:
    def __init__(self, player_name, player_id):
        self.player_name = player_name
        self.player_id = player_id

        self.player_role = None

        self.player_cards = []
        self.player_actions = []

    def add_actions(self, amount):
        self.player_actions = [True for x in range(amount)]





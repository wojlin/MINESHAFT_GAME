class Player:
    def __init__(self, player_name, player_id, config):
        self.player_name = player_name
        self.player_id = player_id

        self.player_role = None

        self.player_cards = []
        self.player_actions = []
        self.leaderboard_pos = 0
        self.rank = 1
        self.last_player_rank = self.rank
        self.rank_url = self.return_rank_url()

    def info(self):
        return {"player_id": self.player_id,
                "rank": self.rank,
                "last_player_rank": self.last_player_rank,
                "rank_url": self.return_rank_url(),
                "last_player_rank_url": self.return_last_player_rank_url(),
                "player_role": self.player_role}

    def add_actions(self, amount):
        self.player_actions = [True for x in range(amount)]

    def upgrade_rank(self, amount):
        self.last_player_rank = self.rank
        self.rank += amount
        self.rank_url = self.return_rank_url()

    def return_rank_url(self):
        return f"/load_image?filename=rank_{self.rank}.png"

    def return_last_player_rank_url(self):
        return f"/load_image?filename=rank_{self.rank}.png"



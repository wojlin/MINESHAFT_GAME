class Card:
    def __init__(self, card_type: str, picture_url):
        self.card_type = card_type
        self.picture_url = picture_url

    def info(self):
        return f"card type: {self.card_type}"


class DirectionCard(Card):
    def __init__(self, way_top: bool, way_right: bool, way_bottom: bool, way_left: bool, overwrite: bool):
        self.way_top = way_top
        self.way_right = way_right
        self.way_bottom = way_bottom
        self.way_left = way_left



        Card.__init__(self, "Tunnel Card")


class ActionCard(Card):
    def __init__(self, action_type: str, action_points: int):
        self.action_type = action_type
        self.action_points = action_points
        Card.__init__(self, "Action Card")


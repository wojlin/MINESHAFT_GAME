class Card:
    def __init__(self, card_type: str, picture_url):
        self.card_type = card_type
        self.picture_url = picture_url

    def info(self):
        return f"card type: {self.card_type}"


class DirectionCard(Card):
    def __init__(self, way_top: bool,
                 way_right: bool,
                 way_bottom: bool,
                 way_left: bool,
                 destructible: bool,
                 overwrite: bool,
                 card_name: str = ""):

        self.way_top = way_top
        self.way_right = way_right
        self.way_bottom = way_bottom
        self.way_left = way_left
        self.destructible = destructible
        self.overwrite = overwrite
        self.__card_name = card_name

        Card.__init__(self, "Tunnel Card", self.__create_filename())

    def __create_filename(self):
        if self.__card_name:
            return self.__card_name + ".png"
        filename = ""
        filename += "top_" if self.way_top else "none_"
        filename += "right_" if self.way_right else "none_"
        filename += "bottom_" if self.way_bottom else "none_"
        filename += "left_" if self.way_left else "none_"
        filename += '.png'
        return filename


class ActionCard(Card):
    def __init__(self, action_type: str, action_points: int):
        self.action_type = action_type
        self.action_points = action_points
        Card.__init__(self, "Action Card", self.__create_filename())

    def __create_filename(self):
        return f"{self.action_type}_{'pos' if self.action_points > 0 else 'neg'}.png"


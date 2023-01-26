import json
import uuid
class Card:
    TUNNEL_TYPE = "Tunnel Card"
    ACTION_TYPE = "Action Card"

    def __init__(self, card_type: str, picture_url: str, card_id:str = ''):
        self.card_type = card_type
        self.picture_url = picture_url
        self.card_id = str(uuid.uuid4()) if card_id == "" else card_id

        self.possible_cards = {"none_none_bottom_left": '╗',
                               "top_none_none_left": '╝',
                               "top_right_none_none": '╚',
                               "none_right_bottom_none": '╔',
                               "none_none_none_none": '╳',
                               "top_right_bottom_left": '╬',
                               "top_right_bottom_none": '╠',
                               "top_none_bottom_left": '╣',
                               "top_right_none_left": '╩',
                               "none_right_bottom_left": '╦',
                               "top_none_bottom_none": '║',
                               "none_right_none_left": '═',
                               "top_none_none_none": '╹',
                               "none_right_none_none": '╺',
                               "none_none_bottom_none": '╻',
                               "none_none_none_left": '╸',
                               "start": '*',
                               "end": '?',
                               "empty": ' ',
                               "false": '-',
                               "true": '+',
                               "objective": '?'}

    def info(self):
        card_vis = ''
        if self.card_type == self.TUNNEL_TYPE:
            card_vis = f"card visualization: [{self.possible_cards[self.picture_url[:-4]]}]"
        elif self.card_type == self.ACTION_TYPE:
            action_type = self.picture_url.split('_')[0]
            points = self.picture_url.split('_')[1][:-4]
            card_vis = f"action type: {action_type}  action effect: {points}"
        else:
            raise Exception("unknown card type")
        return f"card type: {self.card_type}  {card_vis}"

    def is_card_the_same(self, other):
        return True if self.card_id == other.card_id else False


class TunnelCard(Card):
    def __init__(self, way_top: bool,
                 way_right: bool,
                 way_bottom: bool,
                 way_left: bool,
                 destructible: bool,
                 overwrite: bool,
                 empty: bool,
                 card_name: str = "",
                 card_id: str = ""):

        self.way_top = way_top
        self.way_right = way_right
        self.way_bottom = way_bottom
        self.way_left = way_left
        self.destructible = destructible
        self.overwrite = overwrite
        self.empty = empty
        self.__card_name = card_name

        if self.__card_name == "false" or self.__card_name == "true":
            self.end_card = True
            self.__card_name = "objective"

        Card.__init__(self, self.TUNNEL_TYPE, self.__create_filename(), card_id=card_id)

        self.card_info = {"card_directions":
                              {"way_top": self.way_top,
                               "way_right": self.way_right,
                               "way_bottom": self.way_bottom,
                               "way_left": self.way_left
                               },
                          "destructible": self.destructible,
                          "overwrite": self.overwrite,
                          "card_type": self.TUNNEL_TYPE,
                          "card_id": self.card_id,
                          "card_url": self.picture_url
                          }
        self.card_info_js = json.dumps(self.card_info)

    def symbol(self):
        return self.possible_cards[self.picture_url[:-4]]

    def __create_filename(self):
        if self.__card_name:
            return self.__card_name + ".png"
        filename = ""
        filename += "top_" if self.way_top else "none_"
        filename += "right_" if self.way_right else "none_"
        filename += "bottom_" if self.way_bottom else "none_"
        filename += "left" if self.way_left else "none"
        filename += '.png'
        return filename


class ActionCard(Card):
    def __init__(self, action_type: str, is_positive_effect: bool, card_id: str =""):
        self.action_type = action_type
        self.is_positive_effect = is_positive_effect
        self.card_id = card_id
        Card.__init__(self, self.ACTION_TYPE, self.__create_filename(), card_id=card_id)

        self.card_info = {
                          "action_type": self.action_type,
                          "is_positive_effect": self.is_positive_effect,
                          "card_type": self.ACTION_TYPE,
                          "card_id": self.card_id,
                          "card_url": self.picture_url}

        self.card_info_js = json.dumps(self.card_info)

    def __create_filename(self):
        return f"{self.action_type}_{'positive' if self.is_positive_effect else 'negative'}.png"

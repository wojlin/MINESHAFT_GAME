from typing import Dict
import random
import math
import copy

import const
import Cards
from Player import Player


class GameEngine:
    def __init__(self, name: str, game_id: str, players: Dict[str, Player], config: dict):
        self.BOARD_SIZE_X = 12
        self.BOARD_SIZE_Y = 9
        self.name = name
        self.game_id = game_id
        self.players = players
        self.config = config

        self.GOOD_PLAYER = "Solider"
        self.BAD_PLAYER = "Saboteur"

        self.ACTION_CARDS_TYPES_AMOUNT = 3

        self.INITIAL_TUNNEL_CARDS_AMOUNT = 44
        self.INITIAL_ACTION_CARDS_AMOUNT = 27
        self.INITIAL_CARDS_AMOUNT = self.INITIAL_TUNNEL_CARDS_AMOUNT + self.INITIAL_ACTION_CARDS_AMOUNT

        self.SABOTEUR_AMOUNT = self.__assign_saboteurs_amount()
        self.CARDS_PER_PLAYER_AMOUNT = self.__assign_card_amount_per_player()

        self.__assign_player_actions()
        self.__assign_player_roles()
        self.__assign_card_amount_per_player()

        self.cards = self.__create_card_deck()
        self.__assign_initial_cards_to_players()

        self.current_turn_num = 0
        self.turn = list(self.players.values())[self.current_turn_num].player_id

        self.round = 1
        self.ROUNDS_AMOUNT = 3

        self.round_ended = False

        self.EMPTY_CARD = Cards.TunnelCard(False, False, False, False, True, True, True, 'empty')
        self.board = self.__create_game_board()
        self.grid = self.__create_pathfinding_grid()

    def __create_pathfinding_grid(self):
        grid = [[0 for x in range(len(self.board[0])*3)] for y in range(len(self.board)*3)]
        for y in range(len(self.board)):
            for x in range(len(self.board[0])):
                cgrid = self.board[y][x].grid
                for y1 in range(3):
                    for x1 in range(3):
                        grid[y*3+y1][x*3+x1] = cgrid[y1][x1]
        return grid


    def __create_game_board(self):
        board = [[self.EMPTY_CARD for x in range(self.BOARD_SIZE_X)] for y in range(self.BOARD_SIZE_Y)]
        board[4][2] = Cards.TunnelCard(way_top=True,
                                       way_right=True,
                                       way_bottom=True,
                                       way_left=True,
                                       destructible=False,
                                       overwrite=False,
                                       empty=False,
                                       card_name="start")

        board[2][10] = Cards.TunnelCard(way_top=True,
                                       way_right=True,
                                       way_bottom=True,
                                       way_left=True,
                                       destructible=False,
                                       overwrite=False,
                                       empty=False,
                                       card_name="false")

        board[4][10] = Cards.TunnelCard(way_top=True,
                                        way_right=True,
                                        way_bottom=True,
                                        way_left=True,
                                        destructible=False,
                                        overwrite=False,
                                        empty=False,
                                        card_name="true")

        board[6][10] = Cards.TunnelCard(way_top=True,
                                        way_right=True,
                                        way_bottom=True,
                                        way_left=True,
                                        destructible=False,
                                        overwrite=False,
                                        empty=False,
                                        card_name="false")

        return board

    def __assign_player_actions(self):
        for player_id, player_obj in self.players.items():
            player_obj.add_actions(self.ACTION_CARDS_TYPES_AMOUNT)

    def __assign_player_roles(self):
        for player_id, player_obj in self.players.items():
            player_obj.player_role = self.GOOD_PLAYER

        saboteurs = []
        while len(saboteurs) < self.SABOTEUR_AMOUNT:
            player_id, player_obj = random.choice(list(self.players.items()))
            if player_id not in saboteurs:
                saboteurs.append(player_id)
                player_obj.player_role = self.BAD_PLAYER

    def __assign_saboteurs_amount(self):
        return math.floor(len(self.players) / 2.1)

    def __assign_card_amount_per_player(self):
        x = len(self.players)
        return 6 if 3 <= x <= 5 else 4 if 6 <= x <= 10 else 0

    def __create_card_deck(self):
        card_deck = []

        for i in range(self.INITIAL_TUNNEL_CARDS_AMOUNT):
            way_top = bool(random.getrandbits(1))
            way_right = bool(random.getrandbits(1))
            way_bottom = bool(random.getrandbits(1))
            way_left = bool(random.getrandbits(1))
            overwrite = False
            empty = False
            if way_left is False and way_right is False and way_bottom is False and way_top is False:
                empty = True
                overwrite = True
            card_deck.append(Cards.TunnelCard(way_top=way_top,
                                              way_right=way_right,
                                              way_bottom=way_bottom,
                                              way_left=way_left,
                                              destructible=True,
                                              empty=empty,
                                              overwrite=overwrite))

        for i in range(self.INITIAL_ACTION_CARDS_AMOUNT):
            action_type = str(random.randint(0, self.ACTION_CARDS_TYPES_AMOUNT - 1))
            action_effect = bool(random.getrandbits(1))
            card_deck.append(Cards.ActionCard(action_type=action_type, is_positive_effect=action_effect))

        random.shuffle(card_deck)

        return card_deck

    def __assign_initial_cards_to_players(self):
        for player_id, player_obj in self.players.items():
            for i in range(self.CARDS_PER_PLAYER_AMOUNT):
                player_obj.player_cards.append(self.cards[-1])
                self.cards.pop()


class Game(GameEngine):
    def __init__(self, name: str, game_id: str, players: Dict[str, Player], config: dict):
        creation_rules = self.check_game_creation_rules(players)
        if creation_rules[const.MESSAGE_TYPE] == const.ERROR_MESSAGE:
            raise const.InvalidMountOfPlayersException
        GameEngine.__init__(self, name=name, game_id=game_id, players=players, config=config)
        self.update_leaderboard()

    def give_card_from_stack(self, player_id, card_id):
        for card in self.players[player_id].player_cards:
            print(card.info())
        print()
        for i in range(len(self.players[player_id].player_cards)):
            if self.players[player_id].player_cards[i].card_id == card_id:
                print("removing card:", self.players[player_id].player_cards[i].info())
                self.players[player_id].player_cards[i] = copy.deepcopy(self.cards[-1])
        self.cards.pop()

        print()
        for card in self.players[player_id].player_cards:
            print(card.info())

    def update_leaderboard(self):
        positions = []
        for player in self.players:
            current_player = self.players[player]
            positions.append(current_player.rank)
        positions = list(set(positions))
        positions = sorted(positions, reverse=True)

        for player in self.players:
            current_player = self.players[player]
            pos = positions.index(current_player.rank) + 1
            current_player.leaderboard_pos = pos

    def check_winning_conditions(self):
        for y in range(self.BOARD_SIZE_Y):
            for x in range(self.BOARD_SIZE_X):
                card = self.board[y][x]
                if card.end_card and card.goal == "true":
                    if self.board[y][x - 1].way_right:
                        return True
                    if self.board[y - 1][x].way_bottom:
                        return True
                    if self.board[y][x + 1].way_left:
                        return True
                    if self.board[y + 1][x].way_top:
                        return True
        if len(self.cards) == 0:
            return True
        return False

    def dispose_ranks(self, winning_player_id, winning_team):

        ranks = [random.randint(1, 5) for x in range(len(self.players) - self.SABOTEUR_AMOUNT + 1)]

        for player_id in self.players:
            player = self.players[player_id]
            if player.player_id == winning_player_id:
                if player.player_role == winning_team and winning_team == self.GOOD_PLAYER:
                    top_rank = max(ranks)
                    player.upgrade_rank(top_rank)
                    ranks.pop(ranks.index(top_rank))

        for player_id in self.players:
            player = self.players[player_id]
            if player.player_role == winning_team and winning_team == self.BAD_PLAYER:
                player.upgrade_rank(int(math.floor(12/len(self.players))))
            if player.player_role == winning_team and winning_team == self.GOOD_PLAYER:
                rank = random.choice(ranks)
                player.upgrade_rank(rank)
                ranks.pop(ranks.index(rank))

        self.update_leaderboard()

    def end_turn(self, player_id):

        for y in range(self.BOARD_SIZE_Y):
            for x in range(self.BOARD_SIZE_X):
                card = self.board[y][x]
                if card.end_card:
                    if self.board[y][x-1].way_right:
                        card.picture_url = card.goal + ".png"
                    if self.board[y-1][x].way_bottom:
                        card.picture_url = card.goal + ".png"
                    if self.board[y][x+1].way_left:
                        card.picture_url = card.goal + ".png"
                    if self.board[y+1][x].way_top:
                        card.picture_url = card.goal + ".png"

        self.round_ended = self.check_winning_conditions()
        if self.round_ended:
            winning_team = self.BAD_PLAYER if len(self.cards) == 0 else self.GOOD_PLAYER
            self.dispose_ranks(player_id, winning_team)

        self.update_leaderboard()
        self.current_turn_num = self.current_turn_num + 1 if self.current_turn_num < len(self.players) -1 else 0
        self.turn = list(self.players.values())[self.current_turn_num].player_id
        return f"turn ended, now its '{self.players[self.turn].player_name}' turn"

    def check_game_creation_rules(self, players):
        if len(players) < const.MIN_AMOUNT_OF_PLAYERS:
            return {"message_type": const.ERROR_MESSAGE, "message_content": const.PLAYERS_MESSAGES.NOT_ENOUGH_PLAYERS}
        elif len(players) > const.MAX_AMOUNT_OF_PLAYERS:
            return {"message_type": const.ERROR_MESSAGE, "message_content": const.PLAYERS_MESSAGES.TOO_MUCH_PLAYERS}
        else:
            return {"message_type": const.STATUS_MESSAGE, "message_content": const.PLAYERS_MESSAGES.CORRECT_AMOUNT}

    def check_game_tunnel_card_rules(self, card: Cards.TunnelCard, pos_x, pos_y):

        if type(pos_x) != int or type(pos_y) != int:
            return False
        if pos_x < 0 or pos_y < 0:
            return False
        if pos_x > len(self.board[0]) - 1 or pos_y > len(self.board) - 1:
            return False

        place = self.board[pos_y][pos_x]

        if place.destructible is True and card.overwrite is True:
            return True

        if place.empty is False and card.overwrite is False:
            return False
        if place.empty is False and place.destructible is False and card.overwrite is False:
            return False

        test_card_top = None
        test_card_right = None
        test_card_bottom = None
        test_card_left = None

        if pos_y - 1 < 0:
            test_card_top = self.EMPTY_CARD
        if pos_y >= len(self.board) - 1:
            test_card_bottom = self.EMPTY_CARD
        if pos_x - 1 < 0:
            test_card_left = self.EMPTY_CARD
        if pos_x >= len(self.board[0]) - 1:
            test_card_right = self.EMPTY_CARD

        if test_card_top is None:
            test_card_top = self.board[pos_y - 1][pos_x]
        if test_card_right is None:
            test_card_right = self.board[pos_y][pos_x + 1]
        if test_card_bottom is None:
            test_card_bottom = self.board[pos_y + 1][pos_x]
        if test_card_left is None:
            test_card_left = self.board[pos_y][pos_x - 1]

        top_side = test_card_top
        right_side = test_card_right
        bottom_side = test_card_bottom
        left_side = test_card_left

        #print(f"top: {top_side.symbol()}")
        #print(f"right: {right_side.symbol()}")
        #print(f"bottom: {bottom_side.symbol()}")
        #print(f"left: {left_side.symbol()}")

        if top_side.empty and right_side.empty and bottom_side.empty and left_side.empty:
            return False

        if card.way_top and not top_side.way_bottom and not top_side.empty:
            return False
        if card.way_right and not right_side.way_left and not right_side.empty:
            return False
        if card.way_bottom and not bottom_side.way_top and not bottom_side.empty:
            return False
        if card.way_left and not left_side.way_right and not left_side.empty:
            return False

        if not card.way_top and top_side.way_bottom and not top_side.empty:
            return False
        if not card.way_right and right_side.way_left and not right_side.empty:
            return False
        if not card.way_bottom and bottom_side.way_top and not bottom_side.empty:
            return False
        if not card.way_left and left_side.way_right and not left_side.empty:
            return False

        return True

    def update_pathfinding_grid(self, pos_x: int, pos_y: int, card: Cards.TunnelCard):
        for y in range(3):
            for x in range(3):
                self.grid[pos_y * 3 + y][pos_x * 3 + x] = card.grid[y][x]

    def pathfinding_grid_info(self):
        grid = ''
        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):
                grid += str(self.grid[y][x]) + ' '
            grid += '\n'
        return grid

    def info(self):
        info_str = f"uuid: {self.game_id}\n" \
                   f"name: {self.name}\n"

        info_str += f"board size: {self.BOARD_SIZE_X}x{self.BOARD_SIZE_Y}\n"

        info_str += f"cards: {self.INITIAL_CARDS_AMOUNT}\n"

        for card in self.cards:
            info_str += card.info() + '\n'

        info_str += f"board:\n[\n"
        for y in range(len(self.board)):
            info_str += '['
            for x in range(len(self.board[y])):
                info_str += f"[{self.board[y][x].symbol()}]"
            info_str += ']\n'

        info_str += f"]\n"

        info_str += f"players:\n[\n"

        for player in self.players:
            player = self.players[player]
            url_base = f"http://{self.config['host']}:{self.config['port']}/game"
            url_args = f"?game_id={self.game_id}&player_id={player.player_id}"

            info_str += f"name: {player.player_name}     id: {player.player_id}   rank:{player.rank}   leaderboard_pos:{player.leaderboard_pos}    url: {url_base + url_args}\n"

        info_str += "]\n"

        url_base = f"http://{self.config['host']}:{self.config['port']}/game/leaderboard"
        url_args = f"?game_id={self.game_id}"
        info_str += f"leaderboard: {url_base}{url_args}"

        info_str += "\n"

        return info_str



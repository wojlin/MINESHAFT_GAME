from dataclasses import dataclass

MESSAGE_TYPE = "message_type"
ERROR_MESSAGE = "error"
STATUS_MESSAGE = "status"


@dataclass
class PLAYERS_MESSAGES:
    NOT_ENOUGH_PLAYERS = "not enough players"
    TOO_MUCH_PLAYERS = "too much players"
    CORRECT_AMOUNT = "correct amount of players"


MIN_AMOUNT_OF_PLAYERS = 3
MAX_AMOUNT_OF_PLAYERS = 10

class InvalidMountOfPlayersException(Exception):
    pass
COLUMN_COUNT = 7
ROW_COUNT = 6
WINDOW_LENGTH = 4

AI_ID = "🔴"
USER_ID = "🔵"
EMPTY_CHAR = "🔲"


def get_player_value(is_max):
    return AI_ID if is_max else USER_ID

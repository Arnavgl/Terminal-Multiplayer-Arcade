# game_utils.py
# Color codes for terminal output
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    DIM = '\033[2m'
    END = '\033[0m'

# Player 1 will be BLUE, Player 2 will be GREEN
PLAYER_COLORS = {
    'Player 1': Colors.BLUE,
    'Player 2': Colors.GREEN
}

def record_game_result(lobbies, lobby_id, game_name, p1_result, p2_result):
    """Record the result of a game in the lobby's history"""
    if lobby_id in lobbies:
        lobbies[lobby_id]['game_history'].append({
            'game': game_name,
            'p1_result': p1_result,
            'p2_result': p2_result
        })
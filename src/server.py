import socket
import threading
import random
import uuid
import re

# Import the game modules
from tic_tac_toe import play_tic_tac_toe
from rock_paper_scissors import play_rps
from number_guessing import play_number_guess
from game_utils import Colors, PLAYER_COLORS

HOST = 'localhost'
PORT = 5555

# We'll now maintain multiple lobbies
lobbies = {}  # lobby_id -> {clients: [], scoreboard: {}, game_history: []}
waiting_players = []  # Players waiting to be matched

def create_lobby():
    """Create a new lobby with a unique ID"""
    lobby_id = str(uuid.uuid4())[:8]
    lobbies[lobby_id] = {
        'clients': [],
        'scoreboard': {'Player 1': 0, 'Player 2': 0},
        'game_history': []  # Store history of all games played
    }
    return lobby_id

def send_scores(p1, p2, scoreboard, player_map):
    """Send scores to both players in a lobby with colored player names"""
    p1_color = PLAYER_COLORS[player_map[p1]]
    p2_color = PLAYER_COLORS[player_map[p2]]
    
    scores = f"\n{Colors.MAGENTA}--- Scoreboard ---{Colors.END}\n"
    scores += f"{p1_color}{player_map[p1]}: {scoreboard['Player 1']}{Colors.END} | "
    scores += f"{p2_color}{player_map[p2]}: {scoreboard['Player 2']}{Colors.END}\n"
    
    try:
        p1.sendall(scores.encode())
        p2.sendall(scores.encode())
    except:
        pass

def visible_length(s):
    """Calculate the visible length of a string, ignoring color codes"""
    # Remove ANSI color codes
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return len(ansi_escape.sub('', s))

def send_comprehensive_scoreboard(p1, p2, lobby_id, player_map):
    """Send a comprehensive scoreboard showing all games played with colors"""
    lobby = lobbies[lobby_id]
    game_history = lobby['game_history']
    scoreboard = lobby['scoreboard']
    
    # Calculate actual wins (excluding draws)
    p1_wins = sum(1 for game in game_history if game['p1_result'] == 'Won')
    p2_wins = sum(1 for game in game_history if game['p2_result'] == 'Won')
    
    p1_color = PLAYER_COLORS[player_map[p1]]
    p2_color = PLAYER_COLORS[player_map[p2]]
    
    # Create table header
    table = f"\n{Colors.MAGENTA}{'='*60}{Colors.END}\n"
    table += f"{Colors.BOLD}COMPREHENSIVE SCOREBOARD{Colors.END}\n"
    table += f"{Colors.MAGENTA}{'='*60}{Colors.END}\n"
    
    # Create header row with proper alignment
    header = f"{Colors.BOLD}{'S.No.':<6} {'Game Name':<20} {player_map[p1]:<15} {player_map[p2]:<15}{Colors.END}"
    table += header + "\n"
    table += f"{Colors.MAGENTA}{'-'*60}{Colors.END}\n"
    
    # Add each game to the table
    for i, game in enumerate(game_history, 1):
        game_name = game['game']
        p1_result = game['p1_result']
        p2_result = game['p2_result']
        
        # Color the results
        p1_display = f"{p1_color}{p1_result}{Colors.END}" if p1_result != "Draw" else p1_result
        p2_display = f"{p2_color}{p2_result}{Colors.END}" if p2_result != "Draw" else p2_result
        
        # Format the row with proper alignment
        row = f"{i:<6} {game_name:<20} "
        
        # Calculate padding for colored results
        p1_padding = 15 - visible_length(p1_display) + len(p1_display)
        p2_padding = 15 - visible_length(p2_display) + len(p2_display)
        
        row += f"{p1_display:<{p1_padding}} {p2_display:<{p2_padding}}"
        table += row + "\n"
    
    # Add totals row with actual wins only (excluding draws)
    table += f"{Colors.MAGENTA}{'-'*60}{Colors.END}\n"
    
    # Format totals with colored numbers
    p1_wins_display = f"{p1_color}{p1_wins}{Colors.END}"
    p2_wins_display = f"{p2_color}{p2_wins}{Colors.END}"
    
    # Calculate padding for colored totals
    p1_wins_padding = 15 - visible_length(p1_wins_display) + len(p1_wins_display)
    p2_wins_padding = 15 - visible_length(p2_wins_display) + len(p2_wins_display)
    
    totals_row = f"{'Total':<6} {'Wins (excl. draws)':<20} "
    totals_row += f"{p1_wins_display:<{p1_wins_padding}} {p2_wins_display:<{p2_wins_padding}}"
    table += totals_row + "\n"
    table += f"{Colors.MAGENTA}{'='*60}{Colors.END}\n"
    
    # Send to both players
    try:
        p1.sendall(table.encode())
        p2.sendall(table.encode())
    except:
        pass  # Handle case where players might have disconnected

def game_menu(p1, p2, lobby_id):
    """Game menu for a specific lobby"""
    lobby = lobbies[lobby_id]
    scoreboard = lobby['scoreboard']
    player_map = {p1: 'Player 1', p2: 'Player 2'}
    
    p1_color = PLAYER_COLORS[player_map[p1]]
    p2_color = PLAYER_COLORS[player_map[p2]]
    
    while True:
        try:
            p1.sendall(f"\n{Colors.MAGENTA}Choose Game:{Colors.END}\n1. Tic-Tac-Toe\n2. Rock-Paper-Scissors\n3. Number Guessing Duel\n4. Quit\n{Colors.BOLD}Enter choice: {Colors.END}".encode())
            p2.sendall(f"{Colors.YELLOW}Waiting for Player 1 to choose a game...{Colors.END}\n".encode())
            choice = p1.recv(1024).decode().strip()

            if choice == '4':
                # Show comprehensive scoreboard before quitting
                send_comprehensive_scoreboard(p1, p2, lobby_id, player_map)
                p1.sendall(f"{Colors.YELLOW}Quitting...{Colors.END}\n".encode())
                p2.sendall(f"{Colors.YELLOW}Player 1 has left. Disconnecting...{Colors.END}\n".encode())
                return False

            p2.sendall(f"{Colors.YELLOW}Player 1 chose game {choice}. Starting the game...{Colors.END}\n".encode())
            p1.sendall(f"{Colors.YELLOW}Starting game {choice}...{Colors.END}\n".encode())

            if choice == '1':
                play_tic_tac_toe(p1, p2, scoreboard, player_map, lobby_id, lobbies)
            elif choice == '2':
                play_rps(p1, p2, scoreboard, player_map, lobby_id, lobbies)
            elif choice == '3':
                play_number_guess(p1, p2, scoreboard, player_map, lobby_id, lobbies)
            else:
                p1.sendall(f"{Colors.RED}Invalid choice. Try again.{Colors.END}\n".encode())
                continue

            send_scores(p1, p2, scoreboard, player_map)  # Show scores after each game
        except:
            break
    return True

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    
    # Add player to waiting list
    waiting_players.append(conn)
    try:
        conn.sendall(f"{Colors.YELLOW}Waiting for another player to join...{Colors.END}\n".encode())
    except:
        waiting_players.remove(conn)
        return
    
    # Check if we have at least 2 players waiting
    while len(waiting_players) >= 2:
        # Create a new lobby
        lobby_id = create_lobby()
        lobby = lobbies[lobby_id]
        
        # Get the first two players from waiting list
        p1 = waiting_players.pop(0)
        p2 = waiting_players.pop(0)
        
        # Add them to the lobby
        lobby['clients'].extend([p1, p2])
        
        # Start the game in a new thread for this lobby
        threading.Thread(target=start_lobby_game, args=(lobby_id, p1, p2)).start()

def start_lobby_game(lobby_id, p1, p2):
    """Start a game session in a specific lobby"""
    try:
        p1.sendall(f"{Colors.GREEN}Game found! Starting...{Colors.END}\n".encode())
        p2.sendall(f"{Colors.GREEN}Game found! Starting...{Colors.END}\n".encode())
        
        # Run the game menu for this lobby
        game_menu(p1, p2, lobby_id)
        
    except Exception as e:
        print(f"[ERROR] in lobby {lobby_id}: {e}")
    finally:
        # Clean up the lobby when done
        if lobby_id in lobbies:
            try:
                p1.close()
            except:
                pass
            try:
                p2.close()
            except:
                pass
            del lobbies[lobby_id]
            print(f"[LOBBY CLOSED] Lobby {lobby_id} closed")

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)  # Allow more simultaneous connections
    print(f"[STARTED] Server is listening on {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    start_server()
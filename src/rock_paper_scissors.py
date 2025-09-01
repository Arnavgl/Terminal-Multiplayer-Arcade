from game_utils import Colors, PLAYER_COLORS

def play_rps(p1, p2, scoreboard, player_map, lobby_id, lobbies):
    valid_moves = ['rock', 'paper', 'scissors']
    
    p1_color = PLAYER_COLORS[player_map[p1]]
    p2_color = PLAYER_COLORS[player_map[p2]]

    while True:
        try:
            p1.sendall(f"{p1_color}Enter Rock, Paper, or Scissors: {Colors.END}".encode())
            p2.sendall(f"{Colors.YELLOW}Waiting for Player 1 to choose...{Colors.END}\n".encode())
            move1 = p1.recv(1024).decode().strip().lower()

            if move1 not in valid_moves:
                p1.sendall(f"{Colors.RED}Invalid move. Try again.{Colors.END}\n".encode())
                continue

            p2.sendall(f"{p2_color}Enter Rock, Paper, or Scissors: {Colors.END}".encode())
            p1.sendall(f"{Colors.YELLOW}Waiting for Player 2 to choose...{Colors.END}\n".encode())
            move2 = p2.recv(1024).decode().strip().lower()

            if move2 not in valid_moves:
                p2.sendall(f"{Colors.RED}Invalid move. Try again.{Colors.END}\n".encode())
                continue

            outcome = {
                ("rock", "scissors"): "Player 1 wins!",
                ("scissors", "paper"): "Player 1 wins!",
                ("paper", "rock"): "Player 1 wins!",
                ("scissors", "rock"): "Player 2 wins!",
                ("paper", "scissors"): "Player 2 wins!",
                ("rock", "paper"): "Player 2 wins!",
            }

            result = "It's a tie!" if move1 == move2 else outcome.get((move1, move2), "Unexpected outcome.")

            # Color the result message
            if "Player 1 wins" in result:
                result_msg = f"{p1_color}{result}{Colors.END}"
            elif "Player 2 wins" in result:
                result_msg = f"{p2_color}{result}{Colors.END}"
            else:
                result_msg = f"{Colors.YELLOW}{result}{Colors.END}"

            p1.sendall(f"Opponent chose {move2}. {result_msg}\n".encode())
            p2.sendall(f"Opponent chose {move1}. {result_msg}\n".encode())

            if "Player 1 wins" in result:
                scoreboard["Player 1"] += 1
                from game_utils import record_game_result
                record_game_result(lobbies, lobby_id, "Rock-Paper-Scissors", "Won", "Lost")
            elif "Player 2 wins" in result:
                scoreboard["Player 2"] += 1
                from game_utils import record_game_result
                record_game_result(lobbies, lobby_id, "Rock-Paper-Scissors", "Lost", "Won")
            else:
                from game_utils import record_game_result
                record_game_result(lobbies, lobby_id, "Rock-Paper-Scissors", "Draw", "Draw")
            return
        except:
            break
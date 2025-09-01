import random
from game_utils import Colors, PLAYER_COLORS

def play_number_guess(p1, p2, scoreboard, player_map, lobby_id, lobbies):
    number = random.randint(1, 100)
    current, other = p1, p2
    
    p1_color = PLAYER_COLORS[player_map[p1]]
    p2_color = PLAYER_COLORS[player_map[p2]]

    while True:
        try:
            current_color = p1_color if current == p1 else p2_color
            current.sendall(f"{current_color}Guess the number (1-100): {Colors.END}".encode())
            other.sendall(f"{Colors.YELLOW}Waiting for opponent to guess...{Colors.END}\n".encode())
            guess = current.recv(1024).decode().strip()

            if not guess.isdigit():
                current.sendall(f"{Colors.RED}Invalid input. Try again.{Colors.END}\n".encode())
                continue

            guess = int(guess)
            if guess == number:
                current_color = p1_color if current == p1 else p2_color
                current.sendall(f"{current_color}Correct! You win!{Colors.END}\n".encode())
                other.sendall(f"{Colors.RED}Opponent guessed the number. You lose!{Colors.END}\n".encode())
                scoreboard[player_map[current]] += 1
                
                # Record game result
                from game_utils import record_game_result
                winner = "Player 1" if current == p1 else "Player 2"
                p1_result = "Won" if winner == "Player 1" else "Lost"
                p2_result = "Won" if winner == "Player 2" else "Lost"
                record_game_result(lobbies, lobby_id, "Number Guessing", p1_result, p2_result)
                
                return
            elif guess < number:
                current.sendall(f"{Colors.CYAN}Too low!{Colors.END}\n".encode())
            else:
                current.sendall(f"{Colors.CYAN}Too high!{Colors.END}\n".encode())

            current, other = other, current
        except:
            break
from game_utils import Colors, PLAYER_COLORS

def play_tic_tac_toe(p1, p2, scoreboard, player_map, lobby_id, lobbies):
    board = [' ' for _ in range(9)]
    current, other = p1, p2
    current_symbol, other_symbol = 'X', 'O'
    
    p1_color = PLAYER_COLORS[player_map[p1]]
    p2_color = PLAYER_COLORS[player_map[p2]]

    def send_board():
        board_str = ''
        for i in range(0, 9, 3):
            row = ''
            for j in range(3):
                idx = i + j
                cell = board[idx]
                if cell == 'X':
                    cell = f"{p1_color}X{Colors.END}"
                elif cell == 'O':
                    cell = f"{p2_color}O{Colors.END}"
                else:
                    # Show position number for empty cells with dim effect
                    cell = f"{Colors.DIM}{Colors.WHITE}{idx+1}{Colors.END}"
                row += f"{cell}|"
            board_str += row[:-1] + "\n"  # Remove trailing | and add newline
        try:
            p1.sendall(board_str.encode())
            p2.sendall(board_str.encode())
        except:
            pass

    def check_win(symbol):
        win_combinations = [
            [0,1,2], [3,4,5], [6,7,8],
            [0,3,6], [1,4,7], [2,5,8],
            [0,4,8], [2,4,6]
        ]
        return any(all(board[i] == symbol for i in combo) for combo in win_combinations)

    def check_draw():
        return all(space != ' ' for space in board)

    send_board()
    while True:
        try:
            current_color = p1_color if current == p1 else p2_color
            current.sendall(f"{current_color}Your move ({current_symbol}) (1-9): {Colors.END}".encode())
            other.sendall(f"{Colors.YELLOW}Waiting for opponent to play...{Colors.END}\n".encode())

            move = current.recv(1024).decode().strip()
            if not move.isdigit() or not (1 <= int(move) <= 9) or board[int(move)-1] != ' ':
                current.sendall(f"{Colors.RED}Invalid move. Try again.{Colors.END}\n".encode())
                continue

            board_idx = int(move) - 1  # Convert 1-9 to 0-8 for internal storage
            board[board_idx] = current_symbol
            send_board()

            if check_win(current_symbol):
                current_color = p1_color if current == p1 else p2_color
                current.sendall(f"{current_color}You win!{Colors.END}\n".encode())
                other.sendall(f"{Colors.RED}You lose!{Colors.END}\n".encode())
                scoreboard[player_map[current]] += 1
                
                # Record game result
                from game_utils import record_game_result
                winner = "Player 1" if current == p1 else "Player 2"
                p1_result = "Won" if winner == "Player 1" else "Lost"
                p2_result = "Won" if winner == "Player 2" else "Lost"
                record_game_result(lobbies, lobby_id, "Tic-Tac-Toe", p1_result, p2_result)
                
                return
            elif check_draw():
                current.sendall(f"{Colors.YELLOW}Draw!{Colors.END}\n".encode())
                other.sendall(f"{Colors.YELLOW}Draw!{Colors.END}\n".encode())
                
                # Record game result
                from game_utils import record_game_result
                record_game_result(lobbies, lobby_id, "Tic-Tac-Toe", "Draw", "Draw")
                
                return

            current, other = other, current
            current_symbol, other_symbol = other_symbol, current_symbol
        except:
            break
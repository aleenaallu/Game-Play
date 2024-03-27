from a1_support import *
from typing import Optional
board = [[BLANK_PIECE for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

def is_column_full(column: str) -> bool:
    """Returns True if the given column is full, and False otherwise."""
    return not '-' in column

def is_column_empty(column: str) -> bool:
    """Returns True if the given column is empty, and False otherwise."""
    return not 'X' in column and not 'O' in column

def num_hours() -> float:
    """Return the number of hours spent on the assignment."""
    return 0.0  # Replace 0.0 with the actual number of hours spent

def generate_initial_board() -> list[str]:
    """Return the initial board state without any initial pieces."""
    return ['--------'] * BOARD_SIZE

def display_board(board: list[str]) -> None:
    for row in board:
        for i in range(len(row)):
            print('|' + row[i], end='')
        print('|')
    for i in range(1, len(board[0]) + 1):
        print(' ' + str(i), end='')
    print()


# Example usage
board1 = generate_initial_board()
display_board(board1)

def check_win(board: list[str]) -> Optional[str]:
    def check_line(line: str) -> Optional[str]:
        for i in range(len(line) - 3):
            if line[i] != '-' and line[i] == line[i+1] == line[i+2] == line[i+3]:
                return line[i]
        return None

    def get_column(board: list[str], col: int) -> str:
        return ''.join(board[row][col] for row in range(len(board)))

    # Check rows
    for row in board:
        winner = check_line(row)
        if winner:
            return winner

    # Check columns
    for col in range(len(board[0])):
        column = get_column(board, col)
        winner = check_line(column)
        if winner:
            return winner

    # Check diagonals
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            diagonal1 = ''.join(board[row+i][col+i] for i in range(4))
            winner = check_line(diagonal1)
            if winner:
                return winner

            diagonal2 = ''.join(board[row+i][col+3-i] for i in range(4))
            winner = check_line(diagonal2)
            if winner:
                return winner

    return None

          
def play_game():
    while True:
        board = generate_initial_board()
        players = [PLAYER_1_PIECE, PLAYER_2_PIECE]
        current_player = 0

        while True:
            display_board(board)
            print(PLAYER_1_MOVE_MESSAGE if current_player == 0 else PLAYER_2_MOVE_MESSAGE)
            player_input = get_action()

            if player_input == 'q':
                print("Goodbye!")
                return
            elif player_input == 'h':
                print(HELP_MESSAGE)
                continue
            elif player_input[0] == 'a':
                column_index = int(player_input[1:]) - 1
                if is_column_full(board[column_index]):
                    print(FULL_COLUMN_MESSAGE)
                    continue
                add_piece(board, players[current_player], column_index)

                winner = check_win(board)
                if winner:
                    display_board(board)
                    if winner == players[0]:
                        print(PLAYER_1_VICTORY_MESSAGE)
                    else:
                        print(PLAYER_2_VICTORY_MESSAGE)
                    break
                if '-' not in [cell for row in board for cell in row]:
                    display_board(board)
                    print(DRAW_MESSAGE)
                    break
                 
                current_player = (current_player + 1) % 2
            elif player_input[0] == 'r':
                column_index = int(player_input[1:]) - 1
                if is_column_empty(board[column_index]):
                    print(EMPTY_COLUMN_MESSAGE)
                    continue
                remove_piece(board, column_index)
                current_player = (current_player + 1) % 2

        play_again = input(CONTINUE_MESSAGE).strip().lower()
        if play_again != 'y':
            print("Thank you for playing!")
            break

def remove_piece(board: list[str], column_index: int) -> None:
    """Remove the top piece from the specified column."""
    for i in range(BOARD_SIZE - 1, -1, -1):
        if board[i][column_index] != BLANK_PIECE:
            board[i] = board[i][:column_index] + BLANK_PIECE + board[i][column_index + 1:]
            break

def add_piece(board: list[str], piece: str, column_index: int) -> None:
    """Add a piece to the specified column."""
    for i in range(BOARD_SIZE - 1, -1, -1):
        if board[i][column_index] == BLANK_PIECE:
            board[i] = board[i][:column_index] + piece + board[i][column_index + 1:]
            break

def get_action() -> str:
    """Repeatedly prompt the user for a valid action."""
    while True:
        action = input(ENTER_COMMAND_MESSAGE).strip().lower()
        if check_input(action):
            return action
        print(INVALID_FORMAT_MESSAGE)

def check_input(command: str) -> bool:
    if len(command) == 0:
        print(INVALID_FORMAT_MESSAGE)
        return False

    if len(command) == 1 and command.lower() in ['h', 'q']:
        return True

    if len(command) < 2 or len(command) > 3:
        print(INVALID_FORMAT_MESSAGE)
        return False

    action = command[:-1]
    column = command[-1]

    if action.lower() not in ['a', 'r']:
        print(INVALID_FORMAT_MESSAGE)
        return False

    if not column.isdigit() or not 1 <= int(column) <= 8:
        print(INVALID_COLUMN_MESSAGE)
        return False

    return True


def main():
    print("Welcome to Connect Four!")
    play_game()

if __name__ == "__main__":
    main()

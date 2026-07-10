

import math
import random

EMPTY = ' '

WIN_COMBOS = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),   
    (0, 3, 6), (1, 4, 7), (2, 5, 8),   
    (0, 4, 8), (2, 4, 6),              
]


def print_board(board):
    """Print the board, showing position numbers (1-9) in empty cells."""
    def cell(i):
        return board[i] if board[i] != EMPTY else str(i + 1)

    print()
    for r in range(3):
        print(f" {cell(r * 3)} | {cell(r * 3 + 1)} | {cell(r * 3 + 2)} ")
        if r < 2:
            print("-----------")
    print()


def check_winner(board):
    """Return 'X', 'O', or None depending on whether someone has won."""
    for a, b, c in WIN_COMBOS:
        if board[a] != EMPTY and board[a] == board[b] == board[c]:
            return board[a]
    return None


def is_full(board):
    return EMPTY not in board


def available_moves(board):
    return [i for i, mark in enumerate(board) if mark == EMPTY]


def is_game_over(board):
    return check_winner(board) is not None or is_full(board)


def minimax(board, depth, is_maximizing, alpha, beta, ai_mark, human_mark):
    """
    Recursively scores a board position.
    Positive scores favor the AI, negative scores favor the human.
    `depth` is used to prefer faster wins / slower losses.
    """
    winner = check_winner(board)
    if winner == ai_mark:
        return 10 - depth
    if winner == human_mark:
        return depth - 10
    if is_full(board):
        return 0

    if is_maximizing:
        best_score = -math.inf
        for move in available_moves(board):
            board[move] = ai_mark
            score = minimax(board, depth + 1, False, alpha, beta, ai_mark, human_mark)
            board[move] = EMPTY
            best_score = max(best_score, score)
            alpha = max(alpha, score)
            if alpha >= beta:
                break  
        return best_score
    else:
        best_score = math.inf
        for move in available_moves(board):
            board[move] = human_mark
            score = minimax(board, depth + 1, True, alpha, beta, ai_mark, human_mark)
            board[move] = EMPTY
            best_score = min(best_score, score)
            beta = min(beta, score)
            if alpha >= beta:
                break  
        return best_score


def best_move(board, ai_mark, human_mark):
    """Return the index (0-8) of the best move for the AI."""
    best_score = -math.inf
    chosen_move = None

    moves = available_moves(board)
    random.shuffle(moves) 
    for move in moves:
        board[move] = ai_mark
        score = minimax(board, 0, False, -math.inf, math.inf, ai_mark, human_mark)
        board[move] = EMPTY
        if score > best_score:
            best_score = score
            chosen_move = move

    return chosen_move



def get_human_move(board):
    while True:
        raw = input("Enter your move (1-9): ").strip()
        if not raw.isdigit():
            print("Please enter a number between 1 and 9.")
            continue
        pos = int(raw) - 1
        if pos < 0 or pos > 8:
            print("Please enter a number between 1 and 9.")
            continue
        if board[pos] != EMPTY:
            print("That cell is already taken. Choose another.")
            continue
        return pos


def choose_symbol():
    while True:
        choice = input("Choose your symbol — X (you move first) or O (AI moves first): ").strip().upper()
        if choice in ('X', 'O'):
            return choice
        print("Please type X or O.")


def ask_yes_no(prompt):
    while True:
        choice = input(prompt).strip().lower()
        if choice in ('y', 'yes'):
            return True
        if choice in ('n', 'no'):
            return False
        print("Please type y or n.")


def play_one_game():
    human_mark = choose_symbol()
    ai_mark = 'O' if human_mark == 'X' else 'X'

    board = [EMPTY] * 9
    current_mark = 'X'  

    print_board(board)

    while True:
        if current_mark == human_mark:
            pos = get_human_move(board)
            board[pos] = human_mark
        else:
            print("AI is thinking...")
            pos = best_move(board, ai_mark, human_mark)
            board[pos] = ai_mark
            print(f"AI plays position {pos + 1}.")

        print_board(board)

        winner = check_winner(board)
        if winner:
            if winner == human_mark:
                print("Congratulations, you win!")
            else:
                print("The AI wins! Better luck next time.")
            break
        if is_full(board):
            print("It's a draw!")
            break

        current_mark = 'O' if current_mark == 'X' else 'X'


def main():
    print("=" * 45)
    print(" TIC-TAC-TOE vs Unbeatable AI")
    print(" (Minimax algorithm with Alpha-Beta Pruning)")
    print("=" * 45)
    print("\nCells are numbered 1-9 like this:")
    print_board([EMPTY] * 9)

    while True:
        try:
            play_one_game()
        except (KeyboardInterrupt, EOFError):
            print("\n\nGame interrupted. Goodbye!")
            return

        try:
            if not ask_yes_no("Play again? (y/n): "):
                print("Thanks for playing!")
                return
        except (KeyboardInterrupt, EOFError):
            print("\n\nGoodbye!")
            return


if __name__ == "__main__":
    main()
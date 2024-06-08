import random
import os.path
import json

random.seed()

def draw_board(board):
    """
    Prints the game board.

    Args:board (list): The game board.
    """
    for row in board:
        print(' | '.join(row))
        print('-' * 9)

def welcome(board):
    """
    Prints a welcome message and the initial game board.

    Args:board (list): The game board.
    """
    print("Welcome to Noughts and Crosses!")
    draw_board(board)

def initialise_board(board):
    """
    Initializes the game board.

    Args:
        board (list): The game board.

    Returns:
        list: The initialized game board.
    """
    for i in range(3):
        for j in range(3):
            board[i][j] = ' '
    return board

def get_player_move(board):
    """
    Gets the player's move.

    Args:
        board (list): The game board.

    Returns:
        tuple: The row and column of the player's move.
    """
    while True:
        move = input("Enter your move (1-9): ")
        row = (int(move) - 1) // 3
        col = (int(move) - 1) % 3
        if board[row][col] == ' ':
            return row, col

def choose_computer_move(board):
    """
    Chooses the computer's move.

    Args:
        board (list): The game board.

    Returns:
        tuple: The row and column of the computer's move.
    """
    # If the computer can win on the next move, do that
    for i in range(1, 10):
        row, col = (i - 1) // 3, (i - 1) % 3
        if board[row][col] == ' ':
            board[row][col] = 'O'
            if check_for_win(board, 'O'):
                return row, col
            board[row][col] = ' '  # undo the move

    # If the player can win on the next move, block that
    for i in range(1, 10):
        row, col = (i - 1) // 3, (i - 1) % 3
        if board[row][col] == ' ':
            board[row][col] = 'X'
            if check_for_win(board, 'X'):
                board[row][col] = 'O'
                return row, col
            board[row][col] = ' '  # undo the move

    # Take the center if it's available
    if board[1][1] == ' ':
        return 1, 1

    # Take a corner if it's available
    for row, col in [(0, 0), (0, 2), (2, 0), (2, 2)]:
        if board[row][col] == ' ':
            return row, col

    # Take any other cell
    for row in range(3):
        for col in range(3):
            if board[row][col] == ' ':
                return row, col

def check_for_win(board, mark):
    """
    Checks if the given mark has won.

    Args:
        board (list): The game board.
        mark (str): The mark to check.

    Returns:
        bool: True if the given mark has won, False otherwise.
    """
    # check horizontal spaces
    for row in board:
        if row.count(mark) == 3:
            return True

    # check vertical spaces
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] == mark:
            return True

    # check diagonals
    if board[0][0] == board[1][1] == board[2][2] == mark or \
       board[0][2] == board[1][1] == board[2][0] == mark:
        return True

    return False

def check_for_draw(board):
    """
    Checks if the game is a draw.

    Args:
        board (list): The game board.

    Returns:
        bool: True if the game is a draw, False otherwise.
    """
    for row in board:
        if ' ' in row:
            return False
    return True

def play_game(board):
    """
    Plays a game of Noughts and Crosses.

    Args:
        board (list): The game board.

    Returns:
        int: The result of the game (1 if the player wins, -1 if the computer wins, 0 if it's a draw).
    """
    board = initialise_board(board)
    draw_board(board)
    while True:
        row, col = get_player_move(board)
        board[row][col] = 'X'
        draw_board(board)
        if check_for_win(board, 'X'):
            print("Player X wins!")
            return 1
        if check_for_draw(board):
            print("It's a draw!")
            return 0
        row, col = choose_computer_move(board)
        board[row][col] = 'O'
        draw_board(board)
        if check_for_win(board, 'O'):
            print("Computer wins!")
            return -1
        if check_for_draw(board):
            print("It's a draw!")
            return 0

def menu():
    """
    Displays the game menu and gets the player's choice.

    Returns:
        str: The player's choice.
    """
    print("1 - Play the game")
    print("2 - Save score in file 'leaderboard.txt'")
    print("3 - Load and display the scores from the 'leaderboard.txt'")
    print("q - End the program")
    return input("Enter your choice: ")

def load_scores():
    """
    Loads the scores from the leaderboard file.

    Returns:
        dict: The scores.
    """
    if os.path.exists('leaderboard.txt'):
        with open('leaderboard.txt', 'r') as f:
            try:
                leaders = json.load(f)
            except json.decoder.JSONDecodeError:
                leaders = {}
    else:
        leaders = {}
    return leaders

def save_score(score):
    """
    Saves the given score to the leaderboard file.

    Args:
        score (int): To save score .
    """
    name = input("Enter your name: ")
    leaders = load_scores()
    leaders[name] = score
    with open('leaderboard.txt', 'w') as f:
        json.dump(leaders, f)

def display_leaderboard(leaders):
    """
    Displays the leaderboard.

    Args:
        leaders (dict): The scores.
    """
    for name, score in leaders.items():
        print(f"{name}: {score}")

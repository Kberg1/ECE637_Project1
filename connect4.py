import numpy as np


def make_empty_board(n_rows, n_cols):
    """
    Generate an empty connect4 board
    :param n_rows: integer - number of rows on board
    :param n_cols: integer - number of columns on board
    :return: ndarray with shape (n_rows, n_cols) and type int with all entries set to 0
    """
    board = np.zeros((n_rows, n_cols), dtype=int)
    return board


def is_valid_move(board, row, col, n_rows, n_cols):
    """Determine if a move at board[row, col] is valid. Returns true or false.
    :param board: ndarray with shape (n_rows, n_cols) and type int
    :param row: integer - requested row
    :param col: integer - requested column
    :param n_rows: integer - number of rows on the board
    :param n_cols: integer - number of columns on the board
    :return: boolean - True if move would be valid, false otherwise
    """

    # must check several items
    # 1 - is the move in the board boundary?
    # 2 - is the position unoccupied?
    # 3 - is the position in the bottom row or does it have a piece beneath it if not in the bottom row
    if row < 0 or col < 0 or row >= n_rows or col >= n_cols:
        return False
    elif board[row, col] != 0:
        return False
    elif row < (n_rows - 1) and board[row + 1, col] == 0:
        return False
    else:
        return True


def is_horizontal_win(board, row, player):
    """Checks if a move in a given row results in a win in the horizontal direction
    :param board: ndarray with shape (n_rows, n_cols) and type int
    :param row: integer - row to check for horizontal win
    :param player: integer - 1 or 2 representing player 1 or player 2 respectively
    :return: boolean - True if designated player has won, false otherwise
    """

    n_consecutive_pieces = 0
    n_to_win = 4
    n_cols = board.shape[1]
    for column in range(n_cols):
        if board[row, column] == player:
            n_consecutive_pieces += 1
            if n_consecutive_pieces == n_to_win:
                break
        else:
            n_consecutive_pieces = 0

    if n_consecutive_pieces == n_to_win:
        return True
    else:
        return False


def is_vertical_win(board, column, player):
    """Checks if a move in a given column results in a win in the vertical direction
    :param board: ndarray with shape (n_rows, n_cols) and type int
    :param column: integer - column to check for vertical win
    :param player: integer - 1 or 2 representing player 1 or player 2 respectively
    :return: boolean - True if designated player has won, false otherwise
    """

    n_consecutive_pieces = 0
    n_to_win = 4
    n_rows = board.shape[0]
    for row in range(n_rows):
        if board[row, column] == player:
            n_consecutive_pieces += 1
            if n_consecutive_pieces == n_to_win:
                break
        else:
            n_consecutive_pieces = 0

    if n_consecutive_pieces >= n_to_win:
        return True
    else:
        return False


def is_diagonal_win(board, player):
    """Brute force check to see if the most recent move results in a win in the diagonal direction
    :param board: ndarray with shape (n_rows, n_cols) and type int
    :param player: integer - 1 or 2 representing player 1 or player 2 respectively
    :return: boolean - True if designated player has won, false otherwise
    """

    # NOTE that if this is changed, the hardcoded checks below must also be changed
    # I couldn't figure out how to do this other than the unfortunate hardcode
    n_to_win = 4

    n_rows = board.shape[0]
    n_cols = board.shape[1]

    # There is only one way to win diagonally, but two ways to consider it programmatically
    # 1 - top down - start on the top left side of the board, move down and right checking pieces along the way
    # 2 - bottom up - start on the left bottom side of the board, move up and right checking pieces along the way

    # top down. recall that the top left position is [0,0]
    for column in range(n_cols - n_to_win + 1):
        for row in range(n_rows - n_to_win + 1):
            if board[row, column] == board[row + 1, column + 1] == board[row + 2, column + 2] == \
                    board[row + 3, column + 3] == player:
                return True

    # bottom up. recall that the bottom left position is [n_rows-1, 0]
    for column in range(n_cols - n_to_win + 1):
        for row in range(n_rows - n_to_win + 2):
            if board[row, column] == board[row - 1, column + 1] == board[row - 2, column + 2] == \
                    board[row - 3, column + 3] == player:
                return True

    # if here, no diagonal wins detected
    return False


def is_winning_move(board, row, column, player):
    """Wrapper function around the horizontal, vertical, and diagonal win functions to check for winning move
    :param board: ndarray with shape (n_rows, n_cols) and type int
    :param row: integer - row to check for horizontal win
    :param column: integer - column to check for vertical win
    :param player: integer - 1 or 2 representing player 1 or player 2 respectively
    :return: boolean - True if designated player has won, false otherwise
    """
    if is_horizontal_win(board, row, player) or is_vertical_win(board, column, player) or \
            is_diagonal_win(board, player):
        return True
    else:
        return False


def draw_board(board):
    n_rows = board.shape[0]
    n_columns = board.shape[1]
    for row in range(n_rows):
        print(row, '>', end=' ')
        for column in range(n_columns):
            print(board[row, column], end=' ')
        print()

    print('   ', end=' ')
    for column in range(n_columns):
        print('^', end=' ')
    print()
    print('   ', end=' ')
    for column in range(n_columns):
        print(column, end=' ')
    print()


def execute_move(board, row, column, player):
    """
    Places the piece for the designated player in the designated position. Position assumed valid.
    :param board: ndarray with shape (n_rows, n_cols) and type int
    :param row: integer - row to place player's piece
    :param column: integer - column to place player's piece
    :param player: integer - 1 or 2 representing player 1 or player 2 respectively
    :return: None
    """
    board[row, column] = player


def play_game():

    n_rows = 6
    n_columns = 7
    board = make_empty_board(n_rows, n_columns)
    someone_has_won = False
    player = 1

    while True:
        draw_board(board)
        row = int(input('Enter row: '))
        column = int(input('Enter column: '))

        if not is_valid_move(board, row, column, n_rows, n_columns):
            print("Invalid selection")
            continue
        else:
            execute_move(board, row, column, player)
        if is_winning_move(board, row, column, player):
            print("We have a winner!")
            draw_board(board)
            break
        else:
            if player == 1:
                player = 2
            else:
                player = 1


play_game()

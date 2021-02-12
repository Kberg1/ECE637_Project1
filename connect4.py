import numpy as np
import Agent


class Connect4:
    """
    Class to represent the Connect4 Game

    Attributes
    ------------
    board: 2D ndarray representing the game board
    n_rows: integer - number of rows on board. Defaults to 6
    n_cols: integer - number of columns on board. Defaults to 7
    n_to_win: integer - number of consecutive pieces necessary to win. Defaults to 4. See warning in is_diagonal_win
    n_positions_remaining: integer - number of open positions remaining on the board
    ai_agent: integer - 0 -> no AI agent, 1 -> Player 1 is an agent, 2 -> Player 2 is an agent, 3 -> Both are agents
    """
    def __init__(self, n_rows=6, n_cols=7, n_to_win=4, ai_agent=0):
        """
        Generate an empty connect4 board with n_rows and n_cols. Sets attributes.

        :param n_rows: integer - number of rows on board
        :param n_cols: integer - number of columns on board
        :param n_to_win: integer - number of consecutive pieces required for a win
        :param ai_agent: integer - 0 -> no AI agent, 1 -> Player 1 is an AI agent, 2 -> Player 2 is an AI agent
        """
        self.board = np.zeros((n_rows, n_cols), dtype=int)
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.n_to_win = n_to_win
        self.n_positions_remaining = n_rows * n_cols
        self.ai_agent = ai_agent

    def is_valid_move(self, row, col):
        """
        Determine if a move at board[row, col] is valid. Returns true or false.

        :param row: integer - requested row
        :param col: integer - requested column
        :return: True if move would be valid, False otherwise
        """
        # must check several items
        # 1 - is the move in the board boundary?
        # 2 - is the position unoccupied?
        # 3 - is the position in the bottom row or does it have a piece beneath it if not in the bottom row
        if row < 0 or col < 0 or row >= self.n_rows or col >= self.n_cols:
            return False
        elif self.board[row, col] != 0:
            return False
        elif row < (self.n_rows - 1) and self.board[row + 1, col] == 0:
            return False
        else:
            return True

    def is_horizontal_win(self, row, player):
        """
        Checks if a move in a given row results in a win in the horizontal direction

        :param row: integer - row to check for horizontal win
        :param player: integer - 1 or 2 representing player 1 or player 2 respectively
        :return: boolean - True if designated player has won, False otherwise
        """
        n_consecutive_pieces = 0
        for column in range(self.n_cols):
            if self.board[row, column] == player:
                n_consecutive_pieces += 1
                if n_consecutive_pieces == self.n_to_win:
                    break
            else:
                n_consecutive_pieces = 0

        if n_consecutive_pieces == self.n_to_win:
            return True
        else:
            return False

    def is_vertical_win(self, column, player):
        """
        Checks if a move in a given column results in a win in the vertical direction

        :param column: integer - column to check for vertical win
        :param player: integer - 1 or 2 representing player 1 or player 2 respectively
        :return: boolean - True if designated player has won, False otherwise
        """

        n_consecutive_pieces = 0
        for row in range(self.n_rows):
            if self.board[row, column] == player:
                n_consecutive_pieces += 1
                if n_consecutive_pieces == self.n_to_win:
                    break
            else:
                n_consecutive_pieces = 0

        if n_consecutive_pieces >= self.n_to_win:
            return True
        else:
            return False

    def is_diagonal_win(self, player):
        """
        Brute force check to see if the most recent move results in a win in the diagonal direction

        :param player: integer - 1 or 2 representing player 1 or player 2 respectively
        :return: boolean - True if designated player has won, False otherwise
        """

        # VERY IMPORTANT
        # NOTE that if self.n_to_win != 4, the hardcoded checks below must also be changed
        # I couldn't figure out how to do this other than the unfortunate hardcode

        # There is only one way to win diagonally, but two ways to consider it programmatically
        # 1 - top down - start on the top left side of the board, move down and right checking pieces along the way
        # 2 - bottom up - start on the left bottom side of the board, move up and right checking pieces along the way

        # top down. recall that the top left position is [0,0]
        for column in range(self.n_cols - self.n_to_win + 1):
            for row in range(self.n_rows - self.n_to_win + 1):
                if self.board[row, column] == self.board[row + 1, column + 1] == self.board[row + 2, column + 2] == \
                        self.board[row + 3, column + 3] == player:
                    return True

        # bottom up. recall that the bottom left position is [n_rows-1, 0]
        for column in range(self.n_cols - self.n_to_win + 1):
            for row in range(self.n_rows - self.n_to_win + 1, self.n_rows):
                if self.board[row, column] == self.board[row - 1, column + 1] == self.board[row - 2, column + 2] == \
                        self.board[row - 3, column + 3] == player:
                    return True

        # if here, no diagonal wins detected
        return False

    def is_winning_move(self, row, column, player):
        """Wrapper function around the horizontal, vertical, and diagonal win functions to check for winning move
        :param row: integer - row to check for horizontal win
        :param column: integer - column to check for vertical win
        :param player: integer - 1 or 2 representing player 1 or player 2 respectively
        :return: boolean - True if designated player has won, false otherwise
        """
        if self.is_horizontal_win(row, player) or self.is_vertical_win(column, player) or \
                self.is_diagonal_win(player):
            return True
        else:
            return False

    def draw_board(self):
        """
        Draws the board to the terminal

        :return: None
        """
        for row in range(self.n_rows):
            print(row, '>', end=' ')
            for column in range(self.n_cols):
                print(self.board[row, column], end=' ')
            print()

        print('   ', end=' ')
        for column in range(self.n_cols):
            print('^', end=' ')
        print()
        print('   ', end=' ')
        for column in range(self.n_cols):
            print(column, end=' ')
        print()

    def execute_move(self, row, column, player):
        """
        Places the piece for the designated player in the designated position. Position assumed valid.
        :param row: integer - row to place player's piece
        :param column: integer - column to place player's piece
        :param player: integer - 1 or 2 representing player 1 or player 2 respectively
        :return: None
        """
        self.board[row, column] = player
        self.n_positions_remaining -= 1

    def play(self):
        """
        Plays Connect4 via the terminal
        :return: None
        """

        player = 1
        ai_opponent = Agent.Agent(self.ai_agent)
        # TODO - check to see if either player is an AI agent. If so, instantiate agent(s) here

        while True:
            self.draw_board()
            if self.n_positions_remaining == 0:
                print('No moves remaining. The game has ended in a draw.')
                break
            print("Player ", player, "'s turn.", sep='')
            if self.ai_agent != 3 and player != self.ai_agent:
                row = int(input('Enter row: '))
                column = int(input('Enter column: '))
                if self.is_valid_move(row, column):
                    self.execute_move(row, column, player)
                else:
                    print("Invalid selection")
                    continue
            else:
                auto_move = ai_opponent.ai_move(self.board, self.n_positions_remaining)
                row = auto_move[0]
                column = auto_move[1]
                print("Computer chose", auto_move)
                self.execute_move(row, column, self.ai_agent)  # TODO fix hard code

            if self.is_winning_move(row, column, player):
                print("Player", player, "wins!")
                self.draw_board()
                break
            else:
                if player == 1:
                    player = 2
                else:
                    player = 1


game = Connect4(ai_agent=2)
game.play()

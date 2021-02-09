# %%
import numpy as np
from tree import Tree
from tree import Node


class TicTacToe:
    """Tic Tac Toe Board Game

    Attributes
    ------------
    state : 3 x 3 array
        Possible states are as follows:
        '-' - Position has not been played yet
        'x' - Position has been played by maximizer
        'o' - Position has been played by minimizer
    n_positions_open : int
        Number of open positions remaining on the board
    is_a_winner : boolean
        Whether or not there is a winner yet
    maximizer : Object of the Maximizer class
        Player who attempts to maximize the eval function
    minimizer : Object of the Minimizer class
        Player who attempts to minimize the eval function

    Methods
    ---------
    Constructor - Initializes board to all positions open
    play_game - Play the game until there is a winner or the board is full (draw)
    draw_board - Draw the game board based on the current state

    """

    def __init__(self, maximizer, minimizer):
        """Constructor for overall game object

        Description
        -------------
        Initializes state to empty board and is_a_winner flag to False
        Sets the minimizer and maximizer players

        Returns
        ---------
        None
        """

        self.state = np.array([['-', '-', '-'],
                               ['-', '-', '-'],
                               ['-', '-', '-']])
        self.n_rows = self.state.shape[0]
        self.n_cols = self.state.shape[1]
        self.n_positions_open = 9
        self.is_a_winner = False
        self.maximizer = maximizer
        self.minimizer = minimizer

    def draw_board(self):
        for i in range(self.n_rows):
            for j in range(self.n_cols):
                print(self.state[i, j], end=' ')
            print()

    def play_game(self):
        """Maximizer and minimizer take turns playing the game until someone wins"""
        turn_number = 0
        # while self.n_positions_open > 0 and self.is_a_winner == False:
        for _ in range(10):
            if turn_number % 2 == 0:
                self.maximizer.take_turn()
            else:
                self.minimizer.take_turn()

            # draw board here
            self.draw_board()
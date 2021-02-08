# %%
import numpy as np


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

    Methods
    ---------
    Constructor - Initializes board to all positions open
    """

    def __init__(self):
        self.state = np.array([['-', '-', '-'],
                               ['-', '-', '-'],
                               ['-', '-', '-']])
        self.n_positions_open = 9


class Maximizer:
    """Player which attempts to maximize the evaluation function
    """


class Minimizer:
    """Player which attempts to minimize the evaluation function
    """

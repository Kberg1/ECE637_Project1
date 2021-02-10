import numpy as np
from treelib import Tree


class State:
    """
    Object describing the game's state

    Attributes
    ------------
    positions : 2D NumPy array showing status of each board position
    n_pos_open : integer - number of board positions which have not yet been occupied
    """

    def __init__(self, current_player, prev_state=None, row=None, column=None, n_rows=6, n_cols=7):
        if prev_state is None:
            self.positions = np.zeros((n_rows, n_cols), dtype=int)
            self.n_pos_open = n_rows * n_cols
        else:
            self.positions = np.copy(prev_state.positions)
            self.positions[row, column] = current_player
            self.n_pos_open = prev_state.n_pos_open - 1

    def set_state(self, board, n_positions_open):
        """
        Function which sets current state to that reflected by board and n_positions_open

        :param board: 2D NumPy array showing status of each board position
        :param n_positions_open: integer - number of board positions which have not yet been occupied
        :return: None
        """

        self.positions = np.copy(board)
        self.n_pos_open = n_positions_open


class Agent:
    """
    Agent class representing an AI agent utilizing the minimax strategy

    Attributes
    ------------
    player: integer - 1 or 2, represents which player the agent is
    board_n_rows: number of rows in the game's board
    board_n_cols: number of cols in the game's board
    current_state: 2D NumPy array - shows actual board status (future possible states would be in the tree)
    tree: treelib.Tree object - tree which will contain future possible states. Used for decision making.
    """

    def __init__(self, ai_player, board_n_rows=6, board_n_cols=7, n_to_win=4):
        """
        Initializes an agent

        :param ai_player: integer - 1 or 2, represents which player the agent is
        :param board_n_rows: number of rows in the game's board
        :param board_n_cols: number of cols in the game's board
        :param n_to_win: number of consecutive pieces required for a win
        """

        self.player = ai_player
        self.board_n_rows = board_n_rows
        self.board_n_cols = board_n_cols
        self.n_to_win = n_to_win
        self.current_state = None
        self.tree = Tree()

    def set_agent_state(self, board_state, n_pos_open):
        """
        Wrapper function for setting an agent state. Calls State.set_state

        :param board_state: 2D NumPy array showing status of each board position
        :param n_pos_open: integer - number of board positions which have not yet been occupied
        :return: None
        """
        self.current_state.set_state(board_state, n_pos_open)

    def gen_states(self, start_state, current_player):
        """
        Generates all next possible moves from a given state.

        :param start_state: State object - current state of the game
        :param current_player: integer - 1 or 2 - IDs which player would be placing pieces in the generated states
        :return: list of possible next states or None if no new states are possible
        """

        if start_state.n_pos_open == 0:
            return None
        possible_states = []

        for row in range(self.board_n_rows):
            for col in range(self.board_n_cols):
                if self.is_valid_move(row, col, start_state.positions):
                    possible_states.append(State(current_player, start_state, row, col))

        return possible_states

    def is_valid_move(self, row, col, board_positions):
        """
        Determine if a move at board[row, col] is valid. Returns true or false.

        :param row: integer - requested row
        :param col: integer - requested column
        :param board_positions - 2D NumPy array showing status of each board position
        :return: True if move would be valid, False otherwise
        """
        # must check several items
        # 1 - is the move in the board boundary?
        # 2 - is the position unoccupied?
        # 3 - is the position in the bottom row or does it have a piece beneath it if not in the bottom row
        if row < 0 or col < 0 or row >= self.board_n_rows or col >= self.board_n_cols:
            return False
        elif board_positions[row, col] != 0:
            return False
        elif row < (self.board_n_rows - 1) and board_positions[row + 1, col] == 0:
            return False
        else:
            return True

    def generate_tree(self, parent_node, current_player, max_depth):
        """
        Generates the game tree based on the starting state and the next player. Assumes tree has a single root node

        :param parent_node: treelib.Node object - nid of node containing state to branch from
        :param current_player: integer - 1 or 2 representing player 1 or player 2 respectively
        :param max_depth: integer - max depth of tree
        :return: None
        """

        # TODO this needs stop going deeper on a branch if there has been a winning move already
        # VERY IMPORTANT ^^^

        # check depth
        if self.tree.depth(parent_node) == max_depth:
            return
        # avoid unnecessary get_node function calls
        parent_state = self.tree.get_node(parent_node).data
        # generate every possible next state from the current state
        new_states = self.gen_states(parent_state, current_player)
        if new_states is None:
            return
        else:
            n_new_states = len(new_states)
        # create a new node for every possible new state and add it as a child of the parent node
        for i in range(n_new_states):
            self.tree.create_node(parent=parent_node, data=new_states[i])
        # generate next mark
        if current_player == 1:
            next_player = 2
        else:
            next_player = 1
        # call this function on all of the nodes just created
        children = self.tree.children(parent_node)
        for i in range(n_new_states):
            self.generate_tree(children[i].identifier, next_player, max_depth)

    def evaluate(self, node, player):
        # will evaluate similar to way that the connect4 game checks for a winner
        # ie need to check the horizontal, vertical, and diagonal (top down and bottom up) directions for each
        # direction, will count max consecutive pieces for each player
        # points will be awarded to a player if they have consecutive pieces, and points will be taken away from them
        # if their opponent has consecutive pieces

        print(self.player, node)

    def evaluate_horizontal(self, board, player):

        # these dictionaries will contain the number of consecutive streaks of pieces of each size each player has
        # so the key : value will be {size of streak : number of streaks of that size}
        # both the key and the value will be integers
        # dictionary 1 is for player 1, dictionary 2 is for player 2
        streaks_overall = {1: {}, 2: {}}
        # initialize these dictionaries. Note that the 0 key is only there for programmatic convenience later and is not
        # used in score calculation
        for i in range(0, self.n_to_win + 1):
            streaks_overall[1][i] = 0
            streaks_overall[2][i] = 0

        # make another dictionary for easily keeping track of individual streaks
        current_streak = {1: 0, 2: 0}

        if player == 1:
            opponent = 2
        else:
            opponent = 1

        for row in range(self.board_n_rows):
            current_streak[player] = 0
            current_streak[opponent] = 0

            # look at the first piece in each row
            prev_piece = board[row, 0]
            if prev_piece != 0:
                current_streak[prev_piece] += 1  # TODO make sure this equals 1 if hit, then remove comment

            for col in range(1, self.board_n_cols):
                this_piece = board[row, col]

                # 3 possibilities (to consider programmatically) each time another piece is evaluated
                # 1 - the piece doesn't belong to either player (empty spot)
                # 2 - the piece belongs to the same player as the last piece seen
                # 3 - the piece belongs to the other player as compared to the last piece seen
                if this_piece == 0:  # situation 1
                    streaks_overall[player][current_streak[player]] += 1
                    streaks_overall[opponent][current_streak[opponent]] += 1
                    current_streak[player] = 0
                    current_streak[opponent] = 0
                elif this_piece == prev_piece:  # situation 2
                    current_streak[this_piece] += 1
                else:  # situation 3
                    if prev_piece != 0:
                        n = min(current_streak[prev_piece], self.n_to_win)  # avoid OOB indexing
                        print('n =', n)
                        streaks_overall[prev_piece][n] += 1
                        current_streak[prev_piece] = 0

                    current_streak[this_piece] += 1  # TODO make sure this equals 1 if this is hit, then remove comment

                prev_piece = this_piece

        # NOTE would have to manually rewrite scoring piece if n_to_win doesn't equal 4
        # score - each streak gets the following score. 1: 1 pt, 2: 5 pts, 3: 15 pts, 4: 50 pts
        # negative value for all of the opponent pieces
        score_player = streaks_overall[player][1] + 5 * streaks_overall[player][2] + 15 * streaks_overall[player][3] + \
            50 * streaks_overall[player][4]
        score_opponent = streaks_overall[opponent][1] + 5 * streaks_overall[opponent][2] + \
            10 * streaks_overall[opponent][3] + 50 * streaks_overall[opponent][4]
        score_total = score_player - score_opponent
        return score_total


# TODO - this is a test, just delete this before merging to master branch
"""
player = 1
a = Agent(player)
a.current_state = State(player)
a.tree.create_node("Root", "root", data=a.current_state)
a.generate_tree("root", player, 3)
a.tree.show(data_property="positions")
"""

# horizontal eval function test
player = 1
a = Agent(player)
test_state = np.array([[0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 1, 0, 0, 0, 0],
                       [0, 0, 2, 2, 2, 0, 0],
                       [0, 0, 2, 1, 1, 0, 0],
                       [0, 1, 2, 1, 1, 2, 0]], dtype=int)

s = a.evaluate_horizontal(test_state, player)
print(s)

import numpy as np
from treelib import Tree


class State:
    """
    Object describing the game's state

    Attributes
    ------------
    positions : 2D NumPy array showing status of each board position
    n_pos_open : integer - number of board positions which have not yet been occupied
    move : tuple (integer, integer) - row and column of the move that this state was generated with
    """

    def __init__(self, current_player, prev_state=None, row=None, column=None, n_rows=6, n_cols=7):
        if prev_state is None:
            self.positions = np.zeros((n_rows, n_cols), dtype=int)
            self.n_pos_open = n_rows * n_cols
        else:
            self.positions = np.copy(prev_state.positions)
            self.positions[row, column] = current_player
            self.move = (row, column)
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
        self.current_state = State(ai_player)
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
                    # TODO - if this move is a winning move, need to mark the state as such
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

    def streak_accounting(self, prev_piece, this_piece, player, opponent, streaks_overall, current_streak):
        """
        Helper method called by evaluate. Used just to eliminate repeated code

        :param prev_piece: integer - previous piece found
        :param this_piece: integer - most recent piece found
        :param player: integer - 1 or 2, designates which player is which
        :param opponent: integer - 1 or 2, designates which player is which
        :param streaks_overall: dictionary keeping track of overall streak occurrences for each player
        :param current_streak: dictionary keeping track of current streak for each player
        :return:
        """
        # 3 possibilities (to consider programmatically) each time another piece is evaluated
        # 1 - the piece doesn't belong to either player (empty spot)
        # 2 - the piece belongs to the same player as the last piece seen
        # 3 - the piece belongs to the other player as compared to the last piece seen

        # avoid OOB indexing
        current_streak[player] = min(current_streak[player], self.n_to_win)
        current_streak[opponent] = min(current_streak[opponent], self.n_to_win)
        if this_piece == 0:  # situation 1
            streaks_overall[player][current_streak[player]] += 1
            streaks_overall[opponent][current_streak[opponent]] += 1
            current_streak[player] = 0
            current_streak[opponent] = 0
        elif this_piece == prev_piece:  # situation 2
            current_streak[this_piece] += 1
        else:  # situation 3
            if prev_piece != 0:
                streaks_overall[prev_piece][current_streak[prev_piece]] += 1
                current_streak[prev_piece] = 0

            current_streak[this_piece] += 1

    def streak_cleanup(self, player, opponent, streaks_overall, current_streak):
        """
        Helper method called by evaluate. Used just to eliminate repeated code

        :param player: integer - 1 or 2, designates which player is which
        :param opponent: integer - 1 or 2, designates which player is which
        :param streaks_overall: dictionary keeping track of overall streak occurrences for each player
        :param current_streak: dictionary keeping track of current streak for each player
        :return:
        """

        current_streak[player] = min(current_streak[player], self.n_to_win)
        current_streak[opponent] = min(current_streak[opponent], self.n_to_win)
        streaks_overall[player][current_streak[player]] += 1
        streaks_overall[opponent][current_streak[opponent]] += 1
        current_streak[player] = 0
        current_streak[opponent] = 0

    def evaluate(self, board, player):
        """
        Function used to evaluate a position. Only called on leaf nodes during minimax algorithm

        :param board: 2D NumPy array of occupied positions on the board
        :param player: integer - 1 or 2, used to differentiate between player and opponent
        :return:
        """
        # will evaluate similar to way that the connect4 game checks for a winner
        # ie need to check the horizontal, vertical, and diagonal (top down and bottom up) directions for each
        # direction, will count max consecutive pieces for each player
        # points will be awarded to a player if they have consecutive pieces, and points will be taken away from them
        # if their opponent has consecutive pieces

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

        # perform evaluation in horizontal direction
        for row in range(self.board_n_rows):

            # look at the first piece in each row
            prev_piece = board[row, 0]
            if prev_piece != 0:
                current_streak[prev_piece] += 1

            for col in range(1, self.board_n_cols):
                this_piece = board[row, col]
                self.streak_accounting(prev_piece, this_piece, player, opponent, streaks_overall, current_streak)
                prev_piece = this_piece

            # must account for whatever streak was in progress when each row ended
            self.streak_cleanup(player, opponent, streaks_overall, current_streak)

        # perform evaluation in vertical direction
        for col in range(self.board_n_cols):
            prev_piece = board[0, col]

            if prev_piece != 0:
                current_streak[prev_piece] += 1

            for row in range(1, self.board_n_rows):
                this_piece = board[row, col]
                self.streak_accounting(prev_piece, this_piece, player, opponent, streaks_overall, current_streak)
                prev_piece = this_piece

            # must account for whatever streak was in progress when each column ended
            self.streak_cleanup(player, opponent, streaks_overall, current_streak)

        # perform evaluation in top down diagonal direction by first walking up the left side of the board,
        # then walking across the top of the board
        for row in range(self.board_n_rows-2, -1, -1):  # for each top down diagonal starting at left side of board
            c = 1
            r = row + 1

            prev_piece = board[row, 0]
            if prev_piece != 0:
                current_streak[prev_piece] += 1
            while r < self.board_n_rows and c < self.board_n_cols:
                this_piece = board[r, c]
                self.streak_accounting(prev_piece, this_piece, player, opponent, streaks_overall, current_streak)
                prev_piece = this_piece

                r += 1
                c += 1

            # must account for whatever streak was in progress when each diagonal ended
            self.streak_cleanup(player, opponent, streaks_overall, current_streak)

        # keep performing evaluation in top down diagonals, walking across top of board
        for col in range(1, self.board_n_cols - 2):
            r = 1
            c = col + 1

            prev_piece = board[0, col]
            if prev_piece != 0:
                current_streak[prev_piece] += 1
            while r < self.board_n_rows and c < self.board_n_cols:
                this_piece = board[r, c]
                self.streak_accounting(prev_piece, this_piece, player, opponent, streaks_overall, current_streak)
                prev_piece = this_piece

                r += 1
                c += 1

            # must account for whatever streak was in progress when each diagonal ended
            self.streak_cleanup(player, opponent, streaks_overall, current_streak)

        # perform evaluation in bottom up diagonal direction by first walking up the right side of the board,
        # then walking left across the top of the board
        for row in range(self.board_n_rows - 2, -1, -1):  # for each top down diagonal starting at left side of board
            c = self.board_n_cols - 2  # 2nd to last column
            r = row + 1

            prev_piece = board[row, self.board_n_cols-1]
            if prev_piece != 0:
                current_streak[prev_piece] += 1
            while r < self.board_n_rows and c > 0:
                this_piece = board[r, c]
                self.streak_accounting(prev_piece, this_piece, player, opponent, streaks_overall, current_streak)
                prev_piece = this_piece

                r += 1
                c -= 1

            # must account for whatever streak was in progress when each diagonal ended
            self.streak_cleanup(player, opponent, streaks_overall, current_streak)

        # keep performing evaluation in bottom up diagonals, walking left across top of board
        for col in range(self.board_n_cols - 2, 0, -1):
            r = 1
            c = col - 1

            prev_piece = board[0, col]
            if prev_piece != 0:
                current_streak[prev_piece] += 1
            while r < self.board_n_rows and c > 0:
                this_piece = board[r, c]
                self.streak_accounting(prev_piece, this_piece, player, opponent, streaks_overall, current_streak)
                prev_piece = this_piece

                r += 1
                c -= 1

            # must account for whatever streak was in progress when each diagonal ended
            self.streak_cleanup(player, opponent, streaks_overall, current_streak)

        # NOTE would have to manually rewrite scoring piece if n_to_win doesn't equal 4
        # score - each streak gets the following score. 1: 1 pt, 2: 5 pts, 3: 15 pts, 4: 50 pts
        # negative value for all of the opponent pieces
        score_player = 5 * streaks_overall[player][2] + 25 * streaks_overall[player][3] + \
            125 * streaks_overall[player][4]
        score_opponent = 5 * streaks_overall[opponent][2] + \
            50 * streaks_overall[opponent][3] + 200 * streaks_overall[opponent][4]
        score_total = score_player - score_opponent
        return score_total

    def minimax(self, current_node_nid):
        current_node_object = self.tree.get_node(current_node_nid)
        if self.tree.depth(current_node_nid) % 2 == 1:
            is_min_node = True
        else:
            is_min_node = False

        if current_node_object.is_leaf():
            return self.evaluate(current_node_object.data.positions, self.player), -1
        else:
            children_nids = self.tree.is_branch(current_node_nid)
            children_vals = []
            for i in range(len(children_nids)):
                val, throwaway_idx = self.minimax(children_nids[i])
                children_vals.append(val)

        if is_min_node:
            min_child_val = min(children_vals)
            min_child_val_idx = children_vals.index(min_child_val)
            return min_child_val, min_child_val_idx
        else:  # is a max node
            max_child_val = max(children_vals)
            max_child_val_idx = children_vals.index(max_child_val)
            return max_child_val, max_child_val_idx

    def ai_move(self, board_state, n_pos_open):
        # set up for minimax algo run
        # need to build a tree based on the state passed in, deleting the current tree (if it exists)
        if self.tree is not None:
            del self.tree

        # set the max depth of the tree
        depth_limit = 5

        self.set_agent_state(board_state, n_pos_open)
        self.tree = Tree()
        self.tree.create_node("Root", "root", data=self.current_state)
        self.generate_tree("root", self.player, depth_limit)
        value, child = self.minimax("root")
        root_children = self.tree.children("root")
        move = root_children[child].data.move
        return move

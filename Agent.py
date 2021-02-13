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
        self.win = False

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
                    s = State(current_player, start_state, row, col)
                    if self.is_winning_move(row, col, current_player, s.positions):
                        s.win = True
                    possible_states.append(s)
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

    def is_horizontal_win(self, row, player, board):
        """
        Checks if a move in a given row results in a win in the horizontal direction

        :param row: integer - row to check for horizontal win
        :param player: integer - 1 or 2 representing player 1 or player 2 respectively
        :param board: 2d NumPy array with board states
        :return: boolean - True if designated player has won, False otherwise
        """
        n_consecutive_pieces = 0
        for column in range(self.board_n_cols):
            if board[row, column] == player:
                n_consecutive_pieces += 1
                if n_consecutive_pieces == self.n_to_win:
                    break
            else:
                n_consecutive_pieces = 0

        if n_consecutive_pieces == self.n_to_win:
            return True
        else:
            return False

    def is_vertical_win(self, column, player, board):
        """
        Checks if a move in a given column results in a win in the vertical direction

        :param column: integer - column to check for vertical win
        :param player: integer - 1 or 2 representing player 1 or player 2 respectively
        :param board: 2d NumPy array with board states
        :return: boolean - True if designated player has won, False otherwise
        """

        n_consecutive_pieces = 0
        for row in range(self.board_n_rows):
            if board[row, column] == player:
                n_consecutive_pieces += 1
                if n_consecutive_pieces == self.n_to_win:
                    break
            else:
                n_consecutive_pieces = 0

        if n_consecutive_pieces >= self.n_to_win:
            return True
        else:
            return False

    def is_diagonal_win(self, player, board):
        """
        Brute force check to see if the most recent move results in a win in the diagonal direction

        :param player: integer - 1 or 2 representing player 1 or player 2 respectively
        :param board: 2d NumPy array with board states
        :return: boolean - True if designated player has won, False otherwise
        """

        # VERY IMPORTANT
        # NOTE that if self.n_to_win != 4, the hardcoded checks below must also be changed
        # I couldn't figure out how to do this other than the unfortunate hardcode

        # There is only one way to win diagonally, but two ways to consider it programmatically
        # 1 - top down - start on the top left side of the board, move down and right checking pieces along the way
        # 2 - bottom up - start on the left bottom side of the board, move up and right checking pieces along the way

        # top down. recall that the top left position is [0,0]
        for column in range(self.board_n_cols - self.n_to_win + 1):
            for row in range(self.board_n_rows - self.n_to_win + 1):
                if board[row, column] == board[row + 1, column + 1] == board[row + 2, column + 2] == \
                        board[row + 3, column + 3] == player:
                    return True

        # bottom up. recall that the bottom left position is [n_rows-1, 0]
        for column in range(self.board_n_cols - self.n_to_win + 1):
            for row in range(self.board_n_rows - self.n_to_win + 1, self.board_n_rows):
                if board[row, column] == board[row - 1, column + 1] == board[row - 2, column + 2] == \
                        board[row - 3, column + 3] == player:
                    return True

        # if here, no diagonal wins detected
        return False

    def is_winning_move(self, row, column, player, board):
        """Wrapper function around the horizontal, vertical, and diagonal win functions to check for winning move
        :param row: integer - row to check for horizontal win
        :param column: integer - column to check for vertical win
        :param player: integer - 1 or 2 representing player 1 or player 2 respectively
        :param board: 2d NumPy array with board states
        :return: boolean - True if designated player has won, false otherwise
        """
        if self.is_horizontal_win(row, player, board) or self.is_vertical_win(column, player, board) or \
                self.is_diagonal_win(player, board):
            return True
        else:
            return False

    def generate_tree(self, parent_node, current_player, max_depth):
        """
        Generates the game tree based on the starting state and the next player. Assumes tree has a single root node

        :param parent_node: treelib.Node object - nid of node containing state to branch from
        :param current_player: integer - 1 or 2 representing player 1 or player 2 respectively
        :param max_depth: integer - max depth of tree
        :return: None
        """

        # check depth
        if self.tree.depth(parent_node) == max_depth or self.tree.get_node(parent_node).data.win is True:
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

    def evaluate_chunk(self, chunk, player):
        # each chunk is size n_to_win, so positions worth giving a score to, from best to worst are
        # player has all n_to_win spots in this chunk
        # player has n_to_win - 1 spots in this chunk but the remaining spot is open
        # player has n_to_win - 2 spots in this chunk but the remaining two spots are open
        # opponent has n_to_win - 2 spots in this chunk but the remaining two spots are open
        # opponent has n_to_win - 1 spots in this chunk but the remaining spot is open
        # opponent has all n_to_win spots in this chunk

        # convert the ndarray to a list because the list class actually has better methods
        # for counting occurrences of specific values. It could be done in numpy but it would
        # be much less readable and we're not doing math so it seems acceptable
        chunk_list = chunk.tolist()
        score_this_chunk = 0
        if player == 1:
            opponent = 2
        else:
            opponent = 1

        if chunk_list.count(player) == self.n_to_win:
            score_this_chunk += 100
        elif chunk_list.count(player) == self.n_to_win - 1 and chunk_list.count(0) == 1:
            score_this_chunk += 5
        elif chunk_list.count(player) == self.n_to_win - 2 and chunk_list.count(0) == 2:
            score_this_chunk += 2
        elif chunk_list.count(opponent) == self.n_to_win - 2 and chunk_list.count(0) == 2:
            score_this_chunk -= 2
        elif chunk_list.count(opponent) == self.n_to_win - 1 and chunk_list.count(0) == 1:
            score_this_chunk -= 5
        elif chunk_list.count(opponent) == self.n_to_win:
            score_this_chunk -= 100

        return score_this_chunk

    def evaluate(self, board, player):
        # for every row, score n_to_win positions at a time
        # previous eval fx did not take into account whether or not is was possible get a sufficient streak
        # from any given streak of 2 or 3 (ie scored the same even if the pieces were blocked from winning on both
        # sides)
        # this method will now look at each n_to_win sized position and tally a score considering
        # both players' positions as well as open positions

        score = 0
        # center = board[:, self.board_n_cols//2].tolist()
        # score += center.count(player) * 2

        # evaluate in the horizontal direction
        for row in range(self.board_n_rows):
            for column in range(self.board_n_cols - self.n_to_win + 1):  # note indexing stops with space to check
                chunk = board[row, column:column + self.n_to_win]
                score += self.evaluate_chunk(chunk, player)

        # evaluate in the vertical direction
        for column in range(self.board_n_cols):
            for row in range(self.board_n_rows - self.n_to_win + 1):  # note indexing again
                chunk = board[row:row + self.n_to_win, column]
                score += self.evaluate_chunk(chunk, player)

        # top down diagonals
        for row in range(self.board_n_rows - self.n_to_win + 1):
            for column in range(self.board_n_cols - self.n_to_win + 1):
                chunk = np.array([board[row, column], board[row + 1, column + 1], board[row + 2, column + 2],
                                  board[row + 3, column + 3]])
                score += self.evaluate_chunk(chunk, player)

        # bottom up diagonals
        for row in range(self.board_n_rows - 1, self.n_to_win + 2, -1):
            for column in range(self.board_n_cols - self.n_to_win + 1):
                chunk = np.array([board[row, column], board[row - 1, column + 1], board[row - 2, column + 2],
                                  board[row - 3, column + 3]])
                score += self.evaluate_chunk(chunk, player)

        return score

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
            repeats = [children_vals[i] for i in range(len(children_vals)) if children_vals[i] == min_child_val]
            if len(repeats) > 1:
                repeat_indices = [i for i in range(len(children_vals)) if children_vals[i] == min_child_val]
                min_child_val_idx = np.random.choice(repeat_indices)
            else:
                min_child_val_idx = children_vals.index(min_child_val)
            return min_child_val, min_child_val_idx
        else:  # is a max node
            max_child_val = max(children_vals)
            repeats = [children_vals[i] for i in range(len(children_vals)) if children_vals[i] == max_child_val]
            if len(repeats) > 1:
                repeat_indices = [i for i in range(len(children_vals)) if children_vals[i] == max_child_val]
                max_child_val_idx = np.random.choice(repeat_indices)
            else:
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
        print("Player ", self.player, "'s move = column ", move[1], "    value = ", value, sep='')
        print()
        return move

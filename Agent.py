import numpy as np


class Agent:
    """
    Agent class representing an AI agent utilizing the minimax strategy

    Attributes
    ------------
    player: integer - 1 or 2, represents which player the agent is
    n_rows_board: number of rows in the game's board
    n_cols_board: number of cols in the game's board
    """

    def __init__(self, ai_player, n_rows_board=6, n_cols_board=7, n_to_win=4):
        """
        Initializes an agent

        :param ai_player: integer - 1 or 2, represents which player the agent is
        :param n_rows_board: number of rows in the game's board
        :param n_cols_board: number of cols in the game's board
        :param n_to_win: number of consecutive pieces required for a win
        """

        self.player = ai_player
        self.n_rows_board = n_rows_board
        self.n_cols_board = n_cols_board
        self.n_to_win = n_to_win

    def is_valid_move(self, col, board):
        """
        Determine if a move in a given column is valid. Returns None or row

        :param col: integer - requested column
        :param board - 2D NumPy array showing status of each board position
        :return: row number for correct move if move would be valid, None otherwise
        """
        rv = None
        for row in range(self.n_rows_board - 1, -1, -1):  # note that row 5 is the bottom row
            if board[row, col] == 0:
                rv = row
                break
        return rv

    def check_segment_for_winner(self, segment, player):
        """
        Checks a given segment of n_to_win size pieces for a win by designated player

        :param player: integer - player checking for winning pieces
        :param segment: 1d NumPy array representing the game pieces on a particular board segment
        :return: True if player won, False otherwise
        """

        # convert the ndarray to a list because the list class actually has better methods
        # for counting occurrences of specific values. It could be done in numpy but it would
        # be much less readable and we're not doing math so it seems acceptable
        segment_list = segment.tolist()

        if segment_list.count(player) == self.n_to_win:
            rv = True
        else:
            rv = False

        return rv

    def is_winning_state(self, board, player):
        """
        Check a given board state for a win by designated player
        :param player: integer - player checking for winning pieces
        :param board: 2d NumPy array representing the board
        :return: True if player has won, False otherwise
        """

        # evaluate in the horizontal direction
        for row in range(self.n_rows_board):
            for column in range(self.n_cols_board - self.n_to_win + 1):  # note indexing stops with space to check
                segment = board[row, column:column + self.n_to_win]
                win_occurred = self.check_segment_for_winner(segment, player)
                if win_occurred:
                    return True

        # evaluate in the vertical direction
        for column in range(self.n_cols_board):
            for row in range(self.n_rows_board - self.n_to_win + 1):  # note indexing again
                segment = board[row:row + self.n_to_win, column]
                win_occurred = self.check_segment_for_winner(segment, player)
                if win_occurred:
                    return True

        # top down diagonals
        for row in range(self.n_rows_board - self.n_to_win + 1):
            for column in range(self.n_cols_board - self.n_to_win + 1):
                segment = np.array([board[row, column], board[row + 1, column + 1], board[row + 2, column + 2],
                                    board[row + 3, column + 3]])
                win_occurred = self.check_segment_for_winner(segment, player)
                if win_occurred:
                    return True

        # bottom up diagonals
        for row in range(self.n_rows_board - 1, self.n_to_win - 2, -1):
            for column in range(self.n_cols_board - self.n_to_win + 1):
                segment = np.array([board[row, column], board[row - 1, column + 1], board[row - 2, column + 2],
                                    board[row - 3, column + 3]])
                win_occurred = self.check_segment_for_winner(segment, player)
                if win_occurred:
                    return True

        # if here no win has occurred
        return False

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
            score_this_chunk = 100
        elif chunk_list.count(player) == self.n_to_win - 1 and chunk_list.count(0) == 1:
            score_this_chunk = 5
        elif chunk_list.count(player) == self.n_to_win - 2 and chunk_list.count(0) == 2:
            score_this_chunk = 2
        elif chunk_list.count(opponent) == self.n_to_win - 1 and chunk_list.count(0) == 1:
            score_this_chunk = -4

        return score_this_chunk

    def evaluate(self, board, player):
        # for every row, score n_to_win positions at a time
        # previous eval fx did not take into account whether or not is was possible get a sufficient streak
        # from any given streak of 2 or 3 (ie scored the same even if the pieces were blocked from winning on both
        # sides)
        # this method will now look at each n_to_win sized position and tally a score considering
        # both players' positions as well as open positions

        score = 0
        center = board[:, self.n_cols_board//2].tolist()
        score += center.count(player) * 3

        # evaluate in the horizontal direction
        for row in range(self.n_rows_board):
            for column in range(self.n_cols_board - self.n_to_win + 1):  # note indexing stops with space to check
                chunk = board[row, column:column + self.n_to_win]
                score += self.evaluate_chunk(chunk, player)

        # evaluate in the vertical direction
        for column in range(self.n_cols_board):
            for row in range(self.n_rows_board - self.n_to_win + 1):  # note indexing again
                chunk = board[row:row + self.n_to_win, column]
                score += self.evaluate_chunk(chunk, player)

        # top down diagonals
        for row in range(self.n_rows_board - self.n_to_win + 1):
            for column in range(self.n_cols_board - self.n_to_win + 1):
                chunk = np.array([board[row, column], board[row + 1, column + 1], board[row + 2, column + 2],
                                  board[row + 3, column + 3]])
                score += self.evaluate_chunk(chunk, player)

        # bottom up diagonals
        for row in range(self.n_rows_board - 1, self.n_to_win - 2, -1):
            for column in range(self.n_cols_board - self.n_to_win + 1):
                chunk = np.array([board[row, column], board[row - 1, column + 1], board[row - 2, column + 2],
                                  board[row - 3, column + 3]])
                score += self.evaluate_chunk(chunk, player)

        return score

    def is_terminal_state(self, board_state):
        rv = False
        if self.player == 1:
            opponent = 2
        else:
            opponent = 1

        if self.is_winning_state(board_state, self.player) or self.is_winning_state(board_state, opponent) \
                or not np.any(board_state == 0):
            rv = True
        return rv

    def minimax(self, board_state, current_depth, player, alpha, beta, n_nodes):
        max_depth = 5
        if self.is_terminal_state(board_state) is True or current_depth == max_depth:
            if self.is_terminal_state(board_state):
                if self.player == 1:
                    opponent = 2
                else:
                    opponent = 1
                if self.is_winning_state(board_state, self.player):
                    return 1000000000, -1, n_nodes + 1
                elif self.is_winning_state(board_state, opponent):
                    return -1000000000, -1, n_nodes + 1
                else:  # board is full
                    return 0, -1, n_nodes + 1
            else:  # max depth reached
                score = self.evaluate(board_state, self.player)
                return score, -1, n_nodes + 1  # -1 is just a throwaway value

        if current_depth % 2 == 1:
            is_min_node = True
        else:
            is_min_node = False

        if player == 1:
            next_player = 2
        else:
            next_player = 1

        column_list = []
        score_list = []

        for col in range(self.n_cols_board):
            row = self.is_valid_move(col, board_state)
            if row is None:
                continue
            else:
                child_state = np.copy(board_state)
                child_state[row, col] = player
                score, throwaway_val, n_nodes = self.minimax(child_state, current_depth + 1, next_player, alpha, beta,
                                                             n_nodes)
                column_list.append(col)
                score_list.append(score)

                if is_min_node:
                    beta = min(score, beta)
                    if beta <= alpha:
                        if beta == alpha:
                            score_list[len(score_list) - 1] -= 1
                        break
                else:  # is max node
                    alpha = max(score, alpha)
                    if alpha >= beta:
                        if alpha == beta:
                            score_list[len(score_list) - 1] += 1
                        break

        # ensure at least one child had a valid move, if not, just return the evaluation of this node
        # perhaps this could be included in the stop_recursion check for better readability
        if len(score_list) == 0:
            score = self.evaluate(board_state, self.player)
            return score, -1, n_nodes  # -1 is just a throwaway value
        else:
            # check for repeat scores
            if is_min_node:
                score = min(score_list)
            else:
                score = max(score_list)
            repeats = [score_list[i] for i in range(len(score_list)) if score_list[i] == score]
            if len(repeats) > 1:
                repeat_indices = [i for i in range(len(score_list)) if score_list[i] == score]
                score_idx = np.random.choice(repeat_indices)
                best_column = column_list[score_idx]
            else:
                score_idx = score_list.index(score)
                best_column = column_list[score_idx]

            return score, best_column, n_nodes

import numpy as np
from treelib import Node, Tree


class State:
    """
    Attributes
    ------------
    positions : 2D NumPy array showing status of each board position
    n_pos_open : number of squares open
    """

    def __init__(self, prev_state, loc, marker):
        if prev_state is None:
            # TODO randomize first move
            self.positions = np.array([[marker, '-', '-'],
                                       ['-', '-', '-'],
                                       ['-', '-', '-']])
            self.n_pos_open = self.positions.shape[0] * self.positions.shape[1]
        else:
            self.positions = np.copy(prev_state.positions)
            self.positions[loc[0], loc[1]] = marker
            self.n_pos_open = prev_state.n_pos_open - 1


def gen_states(start_state, mark):
    """Generates all next possible moves from a given state.
    :param start_state: current state of the game
    :param mark: 'x' or 'o', mark to be placed on board while generating new states
    :return: list of possible next states or None if no new states are possible
    """

    if start_state.n_pos_open == 0:
        return None
    possible_states = []

    for row in range(3):
        for col in range(3):
            if start_state.positions[row, col] == '-':
                possible_states.append(State(start_state, (row, col), mark))

    return possible_states


def evaluate(state, marker):
    """Evaluate the given state for the given player

    :param state: State object representing the state to be evaluated
    :param marker: 'x' or 'o' representing the player whose status is to be evaluated
    :return: integer representing the value of the provided state
    """




def generate_tree(game_tree, parent_node, mark, max_depth):
    """Generates the game tree based on the starting state and the next player

    :param game_tree: tree being built, assumed not to be empty
    :param parent_node: node containing state to branch from
    :param mark: 'x' or 'o', next marker to place on the board
    :param max_depth: max depth of tree
    :return: None
    """

    # check depth
    if game_tree.depth(parent_node) == max_depth:
        return
    # avoid unnecessary get_node function calls
    parent_state = game_tree.get_node(parent_node).data
    # generate every possible next state from the current state
    new_states = gen_states(parent_state, mark)
    if new_states is None:
        return
    else:
        n_new_states = len(new_states)
    # create a new node for every possible new state and add it as a child of the parent node
    for i in range(n_new_states):
        game_tree.create_node(parent=parent_node, data=new_states[i])
    # generate next mark
    if mark == 'x':
        next_mark = 'o'
    else:
        next_mark = 'x'
    # call this function on all of the nodes just created
    children = game_tree.children(parent_node)
    for i in range(n_new_states):
        generate_tree(game_tree, children[i].identifier, next_mark, max_depth)


s = State(None, (0,0), 'x')
tree = Tree()
tree.create_node("Root", "root", data=s)

generate_tree(tree, "root", 'o', 3)
tree.show(data_property="positions")

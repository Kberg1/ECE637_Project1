from tree import Tree
from tree import Node
import numpy as np

def get_new_state(current_state, next_char):
    """Generates a new state from the given state or returns false if not possible. No eval or heuristics yet.

    :param current_state: instance of State class
    :param next_char: indicates if next move is an 'x' or an 'o'
    :return: new state or false if no new states possible
    """
    dimensions = current_state.shape
    found_new_state = False
    for row in range(dimensions[0]):
        for column in range(dimensions[1]):
            if current_state[row, column] == '-':
                new_state = np.copy(current_state)
                new_state[row, column] = next_char
                found_new_state = True
                break
        if found_new_state:
            break

    if found_new_state:
        return new_state
    else:
        return False


state = np.array([['-', '-', '-'],
                  ['-', '-', '-'],
                  ['-', '-', '-']])

for i in range(0, 9):
    if i % 2 == 0:
        next_symbol = 'x'
    else:
        next_symbol = 'o'
    n_s = get_new_state(state, next_symbol)
    state = n_s
    print(state)

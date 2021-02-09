import numpy as np
from tree import Tree
from tree import Node
from helpers import get_new_state

state = np.array([['-', '-', '-'],
                  ['-', '-', '-'],
                  ['-', '-', '-']])

depth = 4

myTree = Tree(state, depth)

while True:
    i = 0
    if i % 2 == 0:
        next_move = 'x'
    else:
        next_move = 'o'

    next_state = get_new_state(state, next_move)
    myTree.insert(myTree.root, next_state)
    if state == False:
        break
    i += 1

myTree.print_tree(myTree.root)

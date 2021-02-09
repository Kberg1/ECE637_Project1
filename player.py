import numpy as np
from tree import Tree
from tree import Node

class Player:
    """Player which attempts to maximize or minimize the evaluation function"""

    def __init__(self):
        print('created player')
        self.maxDepth = 4

    def make_tree(self, state):
        self.root = Tree(state, self.maxDepth)

        for i in range():
            self.root.insert_node()


class Maximizer(Player):
    """Player which attempts to maximize the evaluation function

    Methods
    ---------
    takeTurn - take a turn, maximizing the eval function
    """

    def take_turn(self):
        print('maximizer taking turn stub')


class Minimizer(Player):
    """Player which attempts to minimize the evaluation function

    Methods
    ---------
    takeTurn - take a turn, minimizing the eval function
    """

    def take_turn(self):
        print('minimizer taking turn stub')
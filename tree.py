import numpy as np

class Node:
    def __init__(self, state):
        """

        :rtype: Node
        """
        self.state = np.copy(state)
        self.children = []


class Tree:
    def __init__(self, state, max_depth):
        self.root = Node(state)
        self.max_depth = max_depth

    def insert(self, parent, state):
        """
        :param parent: Node
        :param state: NumPy array
        :return: None
        """

        parent[len(parent.children)] = Node(state)
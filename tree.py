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

    def insert(self, root, state):
        """Inserts a new node containing the specified state

        :param root: root node of the subtree which is being inserted into
        :param state: state of gameplay - 2D NumPy array
        :return: none
        """

        root.children.insert(len(root.children), Node(state))

    def print_tree(self, root):
        """Prints entire tree

        :param root: root node of current sub tree
        :return: none
        """
        if root is None:
            return
        else:
            for child in range(len(root.children)):
                self.print_tree(root.children[child])
                print(root.state)

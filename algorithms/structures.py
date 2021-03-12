"""
This file holds all the data structures used in the algorithms.
Author: Nerius Ilmonas
Date: 11/03/2021
"""


class Event:
    """
    Represents a tuple (E, T) where E is the event type
    and T is the time at which the event occured.
    """

    def __init__(self, symbol, time):
        self.type = symbol
        self.time = time


class FrequentEpisodePrefixTree:
    """
    Represents a frequent episode prefix tree (FEPT) which stores all
    frequent episodes within a given event sequencec in a space-efficient
    manner. It is a lexicographical rooted directed tree.
    """

    def __init__(self):
        self.root = FrequentEpisodePrefixTreeNode("", None, None)

    def insert(self, label, minimal_occurrences, support):
        """
        Insert a new node into the FEPT.
        """
        node = self.root
        for letter in label:
            if letter in node.children:
                node = node.children[letter]
            else:
                new_node = FrequentEpisodePrefixTreeNode(
                    label, minimal_occurrences, support)
                node.children[letter] = new_node
                node = new_node
        node.is_end = True
        return node

    def dfs(self, node):
        """
        Perform a depth-first search starting from a given node
        """
        if node.is_end:
            self.output.append(node)

        for child in node.children.values():
            self.dfs(child)

    def get_all_frequent_episodes(self):
        """
        Collects all the frequently occurring episodes
        and stores them in a array
        """
        node = self.root
        self.output = []

        self.dfs(node)

        return self.output

    def output_to_file(self):
        """
        Outputs the frequently occurring episodes into
        a .txt file
        """
        frequent_episodes = self.get_all_frequent_episodes()
        with open("frequent_episodes.txt", "w") as f:
            print("Episode\t\t\tSupport", file=f)
            for episode in frequent_episodes:
                print(f"{episode.label:<5}{episode.support:>12}", file=f)


class FrequentEpisodePrefixTreeNode:
    """
    Represents a node of the FEPT.
    Stores the nodes label, minimal_occurences set and a set of indices for which
    the minimal_occurrences are also non_overlapping
    """

    def __init__(self, label, minimal_occurrences, support):
        self.label = label
        self.minimal_occurrences = minimal_occurrences
        self.support = support
        self.children = {}
        self.is_end = False

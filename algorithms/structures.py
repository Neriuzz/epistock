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
        self.children = []


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
        self.children = []

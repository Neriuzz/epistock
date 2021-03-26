#!/usr/bin/env python3

"""
Implementation of the MANEPI+ algorithm as described in: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=5694110
Author: Nerius Ilmonas
Date: 09/03/2021
"""

# Import all required data structures
from structures import FrequentEpisodePrefixTree

# Create an empty FETP
FEPT = FrequentEpisodePrefixTree()


def manepi(event_sequence, min_sup, min_conf):
    """
    Performs the MANEPI+ algorithm on a given
    event sequence with a user defined minimum
    support threshold and outputs all the
    frequent episodes and frequent episode rules
    it finds to frequent_episodes.txt and
    episode_rules.txt respectively. 

    args:
        event_sequence: The event sequence to perform the algorithm on.
        min_sup: The minimum support threshold.
        min_conf: The minimum confidence threshold.
    """

    # Set minimum support and confidence
    FEPT.set_min_conf(min_conf)
    FEPT.set_min_sup(min_sup)

    # Find all 1-episodes
    FEPT.set_frequent_one_episodes(find_frequent_one_episodes(event_sequence))

    for event_type, occurrences in FEPT.frequent_one_episodes:
        # For simple 1-episodes, the support value is always just going to be the
        # length of the set of their occurrences
        node = FEPT.insert([event_type], occurrences, len(occurrences))

        # Grow the 1-episode
        grow(node)

    # All frequently occurring episodes and frequent episode rules have now been found
    return FEPT


def find_frequent_one_episodes(event_sequence):
    """
    Finds all the frequent 1-episodes in the event sequence.
    """

    one_episodes = {}

    # Fill occurrence array
    for event in event_sequence:
        if event.type in one_episodes:
            one_episodes[event.type].append([event.time] * 2)
        else:
            one_episodes[event.type] = [[event.time] * 2]

    # Filter out all the episodes that don't have support >= min_sup
    return sorted(list(filter(lambda episode: len(episode[1]) >= FEPT.min_sup, one_episodes.items())))


def grow(prefix_node):
    """
    Expands a given node, adding onto the tree
    all the frequent episodes with the given
    node as a prefix.
    """

    for event_type, occurrences in FEPT.frequent_one_episodes:

        # Concatenate the two episodes
        label = prefix_node.label + [event_type]

        #MANEPI+ Optimisations
        continue_growth = True
        for i in range(1, len(label)):
            suffix = label[i:]

            if suffix <= prefix_node.label and not FEPT.exists(suffix):
                continue_growth = False
                break

        if not continue_growth:
            continue

        # Grow our pattern and get the minimal occurrences of the new pattern
        minimal_occurrences = concat_minimal_occurrences(
            prefix_node.minimal_occurrences, occurrences)

        # If we have less minimal occurrences than the min_sup
        # we will also have less minimal and non-overlapping
        # occurrences than the min_sup, so we can skip
        # this episode growth
        if len(minimal_occurrences) < FEPT.min_sup:
            continue

        # Check if the pattern is considered frequent (support >= min_sup)
        support = calculate_support(minimal_occurrences)
        if support >= FEPT.min_sup:

            # If it is, create a new FEPT node and add it as a child of the current node
            node = FEPT.insert(label, minimal_occurrences, support)

            # Grow the new pattern further
            grow(node)

    # All frequent patterns have now been found
    return


def concat_minimal_occurrences(prefix_minimal_occurrences, occurrences):
    """
    Computes the minimal occurences for a concatenation of episodes
    """

    # Initialise required variables
    concat_minimal_occurrences = []
    prefix_minimal_occurrences_length = len(prefix_minimal_occurrences)
    i = 0

    for occurrence in occurrences:
        for j in range(i, prefix_minimal_occurrences_length):
            # Find first [t's, t'e] s.t. tje < t's and tj+1e > t's
            if prefix_minimal_occurrences[j][1] < occurrence[0] and (j == prefix_minimal_occurrences_length - 1 or (j != prefix_minimal_occurrences_length - 1 and prefix_minimal_occurrences[j + 1][1] >= occurrence[0])):
                concat_minimal_occurrences.append(
                    [prefix_minimal_occurrences[j][0], occurrence[0]])
                i = j
                break

    return concat_minimal_occurrences


def calculate_support(occurrences):
    """
    Computes the cardinality of the first
    largest set of minimal and non-overlapping
    occurrences => Support value of the episode
    """

    i = 0
    j = 1
    support = 1
    length = len(occurrences)
    while j < length:
        for k in range(j, length):
            if occurrences[i][1] < occurrences[k][0]:
                support += 1
                i = k
                j = i + 1
                continue

            j += 1

    return support

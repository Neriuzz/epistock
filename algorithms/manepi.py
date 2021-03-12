#!/usr/bin/env python3

"""
Implementation of the MANEPI algorithm as described in: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=5694110
Author: Nerius Ilmonas
Date: 09/03/2021
"""

# Import all required data structures
from structures import Event, FrequentEpisodePrefixTree, FrequentEpisodePrefixTreeNode


def manepi(event_sequence, min_sup, event_types):
    """
    Performs the MANEPI+ algorithm on a given
    event sequence with a defined support
    threshold and returns the results
    frequent episode prefix tree.

    args:
        event_sequence: The event sequence to perform the algorithm on.
        min_sup: The minimum support threshold.
    """

    # Create an empty FETP
    fept = FrequentEpisodePrefixTree()

    # Find all 1-episodes
    frequent_one_episodes = find_frequent_one_episodes(
        event_sequence, event_types, min_sup)

    for event_type, occurrences in frequent_one_episodes.items():
        node = FrequentEpisodePrefixTreeNode(
            event_type, occurrences, [i for i in range(len(occurrences))])
        fept.children.append(node)

        grow(node, frequent_one_episodes, min_sup)


def find_frequent_one_episodes(event_sequence, event_types, min_sup):
    """
    Finds all the frequent 1-episodes in the event sequence.
    """
    # Create a dictionary of event_types mapped to occurrences
    frequent_one_episodes = {event_type: [] for event_type in event_types}

    # Fill in the occurrence array
    for event in event_sequence:
        frequent_one_episodes[event.type].append([event.time] * 2)

    # Filter out all the episodes that don't have sup(epi) >= min_sup
    return dict(filter(lambda episode: len(episode[1]) >= min_sup, frequent_one_episodes.items()))


def grow(prefix_node, frequent_one_episodes, min_sup):
    """
    Expands a given node, adding onto the tree
    all the frequent episodes with the given
    node as a prefix.
    """
    for event_type, occurrences in frequent_one_episodes.items():

        # Grow our pattern and get the minimal occurrences of the new pattern
        node_label, minimal_occurrences = concat_minimal_occurrences(
            prefix_node, event_type, occurrences)

        # If the pattern has no minimal occurrences, don't try to grow it
        if not minimal_occurrences:
            continue

        print(node_label)

        # Get the minimal and non-overlapping occurrences of our new pattern
        minimal_and_non_overlapping_occurrences = get_earliest_mano(
            minimal_occurrences)

        # Check if the pattern is considered frequent
        if len(minimal_and_non_overlapping_occurrences) >= min_sup:

            # If it is, create a new FEPT node and add it as a child of the current node
            node = FrequentEpisodePrefixTreeNode(
                node_label, minimal_occurrences, minimal_and_non_overlapping_occurrences)
            prefix_node.children.append(node)

            # Grow the new pattern further
            grow(node, frequent_one_episodes, min_sup)

    # All frequent patterns have now been found
    return


def concat_minimal_occurrences(episode_a, label, occurrences):
    """
    Computes the minimal occurences for a concatenation of episodes
    """

    # Create new label and initialise minimal occurrences array
    label = episode_a.label + label
    b_minimal_occurrences = []
    a_minimal_occurrences = episode_a.minimal_occurrences
    a_minimal_occurrences_length = len(a_minimal_occurrences)
    i = 0

    for occurrence in occurrences:
        for j in range(i, a_minimal_occurrences_length):
            if j < a_minimal_occurrences_length - 1 and a_minimal_occurrences[j][-1] < occurrence[0] and a_minimal_occurrences[j + 1][-1] >= occurrence[0]:
                b_minimal_occurrences.append(
                    [a_minimal_occurrences[j][0], occurrence[0]])
                i = j
                break

            elif j >= a_minimal_occurrences_length - 1 and a_minimal_occurrences[j][-1] < occurrence[0]:
                b_minimal_occurrences.append(
                    [a_minimal_occurrences[j][0], occurrence[0]])
                i = j
                break

    return label, b_minimal_occurrences


def get_earliest_mano(occurrences):
    """
    Computes the earliest minimal
    and non-overlapping occurrences
    from a minimal occurrence set.
    """

    i = 0
    j = 1
    b_minimal_and_non_overlapping_occurrences = [i]
    length = len(occurrences)
    while j < length - 1:
        for k in range(j, length):
            if occurrences[i][-1] < occurrences[k][0]:
                b_minimal_and_non_overlapping_occurrences.append(k)
                i = k
                j = i + 1

            j += 1

    return b_minimal_and_non_overlapping_occurrences

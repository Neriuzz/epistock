"""
Testing for the MANEPI+ algorithm.

Author: Nerius Ilmonas
Date: 24/03/2021
"""

from algorithms import manepi
from algorithms.sax import get_alphabet
from structures import Event
import random
import time
import matplotlib.pyplot as plt


def event_sequence_size_test():
    # Here we simply increase the size of the
    # event sequence each test

    event_types = get_alphabet(5)
    min_conf = 1

    times = []
    sizes = []
    for i in range(15):
        event_sequence_size = 2**(i + 1) * 100
        min_sup = int(0.5 * event_sequence_size)
        event_sequence = [Event(random.choice(event_types), j)
                          for j in range(event_sequence_size)]

        t1 = time.time_ns()

        manepi(event_sequence, min_sup, min_conf)

        t2 = time.time_ns()

        time_taken = (t2 - t1) / 1e9

        times.append(time_taken)
        sizes.append(event_sequence_size)

    return times, sizes


def event_types_size_test():
    # Here we test how the algorithm scales with the amount of event
    # types that are possible

    min_conf = 1

    times = []
    sizes = []
    for i in range(15):
        event_types = get_alphabet(2**(i + 1) * 100)
        event_sequence = [Event(random.choice(event_types), j)
                          for j in range(len(event_types))]
        min_sup = int(0.5 * len(event_sequence))

        t1 = time.time_ns()

        manepi(event_sequence, min_sup, min_conf)

        t2 = time.time_ns()

        time_taken = (t2 - t1) / 1e9

        times.append(time_taken)
        sizes.append(len(event_types))

    return times, sizes


def frequent_episodes_size_test():
    # For this test, since the amount of frequent episodes is inversely proportional to the min_sup,
    # we set the min_sup to smaller and smaller values each test.

    event_types = get_alphabet(5)
    event_sequence = [Event(random.choice(event_types), j)
                      for j in range(1000)]
    min_conf = 1

    times = []
    sizes = []
    for i in range(100):

        min_sup = (110 - i - 1)
        t1 = time.time_ns()

        n_frequent_episodes = manepi(
            event_sequence, min_sup, min_conf).n_frequent_episodes

        t2 = time.time_ns()

        time_taken = (t2 - t1) / 1e9

        times.append(time_taken)
        sizes.append(n_frequent_episodes)

    return times, sizes


def test_manepi():
    fig = plt.figure()
    ax1 = fig.add_subplot(131)
    ax2 = fig.add_subplot(132)
    ax3 = fig.add_subplot(133)

    # Test scaling with event sequence size
    times_test1, sizes_test1 = event_sequence_size_test()
    ax1.plot(sizes_test1, times_test1)

    # Set labels
    ax1.set_title("Scaling with Event Sequence Size")
    ax1.set_xlabel("Event sequence size")
    ax1.set_ylabel("Time taken (s)")

    # Test scaling with number of event types
    times_test2, sizes_test2 = event_types_size_test()
    ax2.plot(sizes_test2, times_test2)

    # Set labels
    ax2.set_title("Scaling with Number of Event Types")
    ax2.set_xlabel("Number of event types")
    ax2.set_ylabel("Time taken (s)")

    # Test scaling with number of frequent episodes
    times_test3, sizes_test3 = frequent_episodes_size_test()
    ax3.plot(sizes_test3, times_test3)

    # Set labels
    ax3.set_title("Scaling with Number of Frequent Episodes")
    ax3.set_xlabel("Number of frequent episodes")
    ax3.set_ylabel("Time taken (s)")

    plt.show()

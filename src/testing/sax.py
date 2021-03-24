"""
Testing for the SAX algorithm.

Author: Nerius Ilmonas
Date: 24/03/2021
"""

from algorithms import sax
import random
import time
import matplotlib.pyplot as plt


def data_size_test():
    # Testing against size of data
    times = []
    sizes = []

    word_length = 500
    alphabet_size = 5
    for i in range(10):
        # Setup required variables
        data_length = 2**(i + 1) * 1000
        data = [random.random() for _ in range(data_length)]

        # Start timing
        t1 = time.time_ns()

        # Perform SAX
        sax(data, word_length, alphabet_size)

        # End timing
        t2 = time.time_ns()

        time_taken = (t2 - t1) / 1e9
        times.append(time_taken)
        sizes.append(data_length)

    return times, sizes


def word_length_test():
    # Testing against word length
    times = []
    sizes = []

    # Create random data set
    data = [random.random() for _ in range(10000)]

    alphabet_size = 5
    for i in range(10):
        # Setup required variables
        word_length = 2**(i + 1)

        # Start timing
        t1 = time.time_ns()

        # Perform SAX
        sax(data, word_length, alphabet_size)

        # End timing
        t2 = time.time_ns()

        time_taken = (t2 - t1) / 1e9
        times.append(time_taken)
        sizes.append(word_length)

    return times, sizes


def alphabet_size_test():
    # Testing against alphabet size
    times = []
    sizes = []

    # Create random data set
    data = [random.random() for _ in range(1000)]

    word_length = 500
    for i in range(10):
        # Setup required variables
        alphabet_size = 2**(i + 1) * 5

        # Start timing
        t1 = time.time_ns()

        # Perform SAX
        sax(data, word_length, alphabet_size)

        # End timing
        t2 = time.time_ns()

        time_taken = (t2 - t1) / 1e9
        times.append(time_taken)
        sizes.append(alphabet_size)

    return times, sizes


def test_sax():

    fig = plt.figure()
    ax1 = fig.add_subplot(131)
    ax2 = fig.add_subplot(132)
    ax3 = fig.add_subplot(133)

    # Test scaling with data size
    times_test1, sizes_test1 = data_size_test()
    ax1.plot(sizes_test1, times_test1)

    # Set labels
    ax1.set_title("Scaling with Data Set Size")
    ax1.set_xlabel("Data set size")
    ax1.set_ylabel("Time taken (s)")

    # Test scaling with word length
    times_test2, sizes_test2 = word_length_test()
    ax2.plot(sizes_test2, times_test2)

    # Set labels
    ax2.set_title("Scaling with Word Length")
    ax2.set_xlabel("Word length")
    ax2.set_ylabel("Time taken (s)")

    # Test scaling with alphabet size
    times_test3, sizes_test3 = alphabet_size_test()
    ax3.plot(sizes_test3, times_test3)

    # Set labels
    ax3.set_title("Scaling with Alphabet Size")
    ax3.set_xlabel("Alphabet size")
    ax3.set_ylabel("Time taken (s)")

    plt.show()

"""
Functions for converting csv data into an event sequence
Author: Nerius Ilmonas
Date: 19/03/2021
"""

import csv
from algorithms import sax
from structures import Event


def get_time_series():
    """
    Extract the time series sequence from our csv file
    by taking the average price for each day (high + low) / 2
    """

    with open("stock_data.csv", "r") as f:
        reader = csv.reader(f)
        _ = next(reader)
        return [(float(line[2]) + float(line[3])) / 2 for line in reader][::-1]


def convert_to_event_sequence(sequence, word_length, alphabet_size):
    """
    Convert our time series sequence into a set of events
    by performing the SAX algorithm
    """

    sax_form = sax(sequence, word_length, alphabet_size)
    return [Event(sax_form[i], i + 1) for i in range(len(sax_form))]

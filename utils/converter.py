"""
Functions for converting csv data into an event sequence
"""

import csv
from algorithms import sax
from structures import Event


def get_time_series():
    with open("stock_data.csv", "r") as f:
        reader = csv.reader(f)
        _ = next(reader)
        return [float(line[1]) for line in reader]


def convert_to_event_sequence(sequence, word_length, alphabet_size):
    sax_form = sax(sequence, word_length, alphabet_size)
    return [Event(sax_form[i], i + 1) for i in range(len(sax_form))]

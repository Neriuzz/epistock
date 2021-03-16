"""
Functions for converting csv data into an event sequence
"""

import csv
from algorithms import sax
from structures import Event


def convert_stock_data(word_length, alphabet_size):
    with open("stock_data.csv", "r") as f:
        reader = csv.reader(f)
        for line in reader:
            pass
        # TODO: Implement conversion to event sequence

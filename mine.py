#!/usr/bin/env python3

"""
This script pre-processes data and mines it using a specified algorithm and specified parameters
Author: Nerius Ilmonas
Date: 09/03/2021 
"""

import sys
import os.path
from algorithms import manepi
from utils import get_stock_data, get_time_series, convert_to_event_sequence


VALID_ARGS = ["-w", "--word-length", "-a", "--alphabet_size",
              "-s", "--min-sup", "-c", "--min-conf", "-h", "--help"]


def print_help():
    print(
        """
    Tool to discover frequently occurring episodes and frequent episode rules for a specific stock ticker.

    *! Before using this tool please make sure you have set an environment variable ALPHA_VANTAGE_KEY to your alpha vantage API key. !*

    USAGE:
        python mine.py <TICKER> <OPTIONS>
        python mine.py -h or python mine.py --help

    OPTIONS:
        -h or --help: Displays this message.
        -w or --word-length: Set the word length parameter for the SAX algorithm. (Default: 0.5 * Length of data)
        -a or --alphabet-size: Set the alphabet size parameter for the SAX algorithm. (Default: 5)
        -s or --min-sup: Set the minimum support value for MANEPI. (Default 0.01 * Length of event sequence)
        -c or --min-conf: Set the minimum confidence value for MANEPI. (Default: 0.75)

    INFORMATION:
        Author: Nerius Ilmonas
        Email: nerius.ilmonas@kcl.ac.uk
        Version: 1.0
        Date: 16/03/2021
    """
    )
    return


if __name__ == "__main__":

    # Defaults
    alphabet_size = 26
    min_conf = 0.75
    min_sup_multiplier = 0.01
    word_length_multiplier = 0.75

    word_length = 0
    min_sup = 0

    ticker = ""

    # Handle options
    if "-h" in sys.argv or "--help" in sys.argv:
        print_help()
        sys.exit(0)

    if sys.argv[1] in VALID_ARGS:
        raise Exception("Please provide a ticker")

    ticker = sys.argv[1]

    args = sys.argv[1:]

    if "-w" in args or "--word-length" in args:
        try:
            word_length = int(args[args.index("-w") + 1])
        except:
            word_length = int(args[args.index("--word-length") + 1])

    if "-a" in args or "--alphabet-size" in args:
        try:
            alphabet_size = int(args[args.index("-a") + 1])
        except:
            alphabet_size = int(args[args.index("--alphabet-size") + 1])

    if "-s" in args or "--min-sup" in args:
        try:
            min_sup = int(args[args.index("-s") + 1])
        except:
            min_sup = int(args[args.index("--min-sup") + 1])

    if "-c" in args or "--min-conf" in args:
        try:
            min_conf = float(args[args.index("-c") + 1])
        except:
            min_conf = float(args[args.index("--min-conf") + 1])

    # Check if result directory exists, if it doesn't make one
    if not os.path.isdir("results"):
        os.mkdir("results")

    # Download stock data
    if not get_stock_data(ticker):
        print(
            f"Data for ${ticker} has previously been fetched, skipping fetching...")

    # Parse stock data into event sequence
    print("[!] Converting csv data into a sequence...")
    time_series = get_time_series(ticker)

    word_length = word_length if word_length else int(word_length_multiplier *
                                                      len(time_series))

    print("[!] Generating event sequence...")
    event_sequence = convert_to_event_sequence(
        time_series, word_length, alphabet_size)

    # Mine stock data for patterns
    min_sup = min_sup if min_sup else int(
        min_sup_multiplier * len(event_sequence))

    print("[!] Discovering frequent episodes in event sequence...")
    manepi(ticker, event_sequence, min_sup, min_conf)

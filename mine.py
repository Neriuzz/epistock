#!/usr/bin/env python3

"""
This script pre-processes data and mines it using a specified algorithm and specified parameters
Author: Nerius Ilmonas
Date: 09/03/2021 
"""

import sys
from algorithms import manepi
from utils import get_stock_data, convert_stock_data


def print_help():
    print(
        """
    Tool to discover frequently occurring episodes and frequent episode rules for a specific stock ticker.
    
    *! Before using this tool please make sure you have set an environment variable ALPHA_VANTAGE_KEY to your alpha vantage API key. !*

    USAGE:
        python mine.py <TICKER> <INTERVAL> <OPTIONS>

    OPTIONS:
        -h or --help: Displays this message.
        -w or --word-length: Set the word length parameter for the SAX algorithm. (Default: 0.75 * Length of data)
        -a or --alphabet-size: Set the alphabet size parameter for the SAX algorithm. (Default: 10)
        -s or --min-sup: Set the minimum support value for MANEPI.
        -c or --min-conf: Set the minimum confidence value for MANEPI.

    INFORMATION:
        Author: Nerius Ilmonas
        Email: nerius.ilmonas@kcl.ac.uk
        Version: 1.0
        Date: 16/03/2021
    """
        # TODO: Add defaults
    )
    return


if __name__ == "__main__":
    if "-h" in sys.argv or "--help" in sys.argv:
        print_help()
        sys.exit(0)

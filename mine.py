#!/usr/bin/env python3

"""
This script pre-processes data and mines it using a specified algorithm and specified parameters
Author: Nerius Ilmonas
Date: 03/09/2021 
"""

import algorithms
from structures import Event
from api import get_stock_data

seq = [Event("A", 1), Event("A", 2), Event("B", 3), Event("D", 4), Event("A", 5), Event("C", 6), Event("B", 7), Event(
    "B", 8), Event("E", 9), Event("A", 10), Event("B", 11), Event("A", 12), Event("C", 13), Event("E", 14), Event("F", 15)]
algorithms.manepi(seq, 3, 0.75)

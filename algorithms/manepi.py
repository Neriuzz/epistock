#!/usr/bin/env python3

"""
Implementation of the MANEPI algorithm as described in: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=5694110
Author: Nerius Ilmonas
Date: 09/03/2021
"""


class Event:
    """
    Represents a tuple (E, T) where E is the event type and T is the time at which the event occured
    """

    def __init__(self, symbol, time):
        self.type = symbol
        self.time = time


def manepi(sequence, min_sup):
    pass

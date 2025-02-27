#!/usr/bin/env python3

# Implementation of the SAX algorithm, which converts time-series data into a string representation
# Author: Nerius Ilmonas
# Date: 2021/02/28

# Implementation adapted from https://jmotif.github.io/sax-vsm_site/morea/algorithm/SAX.html

import random
from string import ascii_uppercase, ascii_lowercase
from statistics import fmean as mean
from statistics import stdev, NormalDist


def z_normalize(data):
    """ Perform a z-normalization on the data """

    dist = NormalDist(mean(data), stdev(data))
    return [dist.zscore(i) for i in data]


def paa_transform(data, paa_size):
    """ Perform the piecewise aggregate approximation transformation on the data """

    length = len(data)
    # Edge cases
    if paa_size >= length:
        return data
    if paa_size == 1:
        return [mean(data)]
    # If data can be divided into equal parts, perform piecewise constant aggregation
    if length % paa_size == 0:
        # Calculate the segment size
        segment_size = int(length/paa_size)
        # Split data into segments according to segment size and then calculate mean for each segment
        return [mean(data[(i - 1) * segment_size:i * segment_size]) for i in range(1, paa_size + 1)]

    # Otherwise, perform piecewise aggregate approximation
    paa = [0] * paa_size
    for i in range(length * paa_size):
        x = (i // length) + 1
        y = (i // paa_size) + 1
        paa[x - 1] += data[y - 1]

    return [i / length for i in paa]


def paa_to_string(paa, regions, alphabet):
    """ Maps each value in the paa to a region and returns the character string representation """

    string = []
    for i in paa:
        index = 0
        try:
            while(i > regions[index]):
                index += 1
        except:
            pass

        string.append(alphabet[index])

    return string


def sax_transform(paa, alphabet_size):
    """ Generate character regions using inverse cumulative density function then return string representation """

    regions = [NormalDist().inv_cdf((i * 1) / alphabet_size)
               for i in range(1, alphabet_size)]
    return paa_to_string(paa, regions, get_alphabet(alphabet_size))


def sax(data, word_length, alphabet_size):
    """ 
    Perform the symbolic aggregate approximation on a piece of data
    args:
        data: The data to transform
        word_length: The length of the output string
        alphabet_size: The length of the alphabet you want to use, for example, for an alphabet {A, B, C}, alphabet_size = 3
    """
    return sax_transform(paa_transform(z_normalize(data), word_length), alphabet_size)


def get_alphabet(alphabet_size):
    """
    Retrieve the alphabet based on the alphabet_size
    """

    if alphabet_size > 52:
        return [str(i) for i in range(alphabet_size)]
    elif alphabet_size > 26:
        return ascii_uppercase + ascii_lowercase
    else:
        return ascii_uppercase

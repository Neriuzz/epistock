#!/usr/bin/env python3

# Implementation of the SAX algorithm, which converts time-series data into a string representation
# Author: Nerius Ilmonas
# Date: 2021/02/28

# Implementation adapted from https://jmotif.github.io/sax-vsm_site/morea/algorithm/SAX.html

from string import ascii_letters as LETTERS
from scipy.stats import norm


def mean(data):
    """ Calculate the mean of the data """
    return sum(data)/len(data)


def standard_deviation(data):
    """ Calculate the standard deviation of the data """
    m = mean(data)
    l = len(data)
    return (1 / l * sum([(i - m)**2 for i in data]))**.5


def z_normalize(data):
    """ Perform a z-normalization on the data """
    m = mean(data)
    sd = standard_deviation(data)
    return [(i - m)/sd for i in data]


def paa_transform(data, paa_size):
    """ Perform the piecewise aggregate approximation transformation on the data """

    length = len(data)
    # Edge cases
    if paa_size >= length:
        return data
    if paa_size == 1:
        return mean(data)
    # If data can be divided into equal parts, perform piecewise constant aggregation
    if length % paa_size == 0:
        # Calculate the segment size
        segment_size = int(length/paa_size)
        # Split data into segments according to segment size and then calculate mean for each segment
        return [mean(data[(i - 1) * segment_size:i * segment_size]) for i in range(1, paa_size + 1)]

    # Otherwise, perform piecewise aggregate approximation
    paa = [0] * paa_size
    for i in range(length * paa_size):
        x = i // length + 1
        y = i // paa_size + 1
        paa[x - 1] += data[y - 1]

    return [round(i / length, 2) for i in paa]


def paa_to_string(paa, regions):
    """ Maps each value in the paa to a region and returns the character string representation """
    string = ""
    for i in paa:
        index = 0
        try:
            while(i > regions[index]):
                index += 1
        except:
            pass
        string += LETTERS[index]
    return string


def sax_transform(paa, alphabet_size):
    """ Generate character regions using inverse cumulative density function then return string representation"""
    regions = [norm.ppf((i * 1) / alphabet_size)
               for i in range(1, alphabet_size)]
    return paa_to_string(paa, regions)


def sax(data, word_length, alphabet_size):
    """ 
    Perform the symbolic aggregate approximation on a piece of data
    args:
        data: The data to transform
        word_length: The length of the output string
        alphabet_size: The length of the alphabet you want to use, for example, for an alphabet {a, b, c}, word_length = 3
    """
    return sax_transform(paa_transform(z_normalize(data), word_length), alphabet_size)

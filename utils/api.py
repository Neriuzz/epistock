#!usr/bin/env python3

"""
Uses the alpha vantage API to retrieve a large amount of historical
stock price data for a speific marker and saves it to stock_data.csv

Author: Nerius Ilmonas
Date: 15/03/2021
"""


import os
import requests
from time import time

# Get API key from environment variables and create request URL
API_KEY = os.getenv("ALPHA_VANTAGE_KEY")

# Make sure user has set their API key
if not API_KEY:
    raise Exception("Alpha Vantage API key has not been set!")

BASE_URL = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&"


def get_stock_data(ticker):
    """
    Downloads 2 years and 12 months worth of stock
    price data based on a specific a stock ticker and 
    time interval e.g. AAPL 5mins
    """

    # Create folders for data if they don't exist
    if os.path.isdir(f"results/{ticker}"):
        return 0
    else:
        os.mkdir(f"results/{ticker}")

    url = BASE_URL + \
        f"symbol={ticker}&outputsize=full&datatype=csv&apikey={API_KEY}"

    # Initialise timer
    t1 = time()

    print(f"Fetching ${ticker} data...")

    # Initialise .csv file
    with open(f"results/{ticker}/{ticker}.csv", "w") as f:
        # Write .csv headers
        print("time,open,high,low,close,volume", file=f)
        data = "".join(requests.get(url).text.split("\n")[1:])

        if not data:
            raise Exception("Invalid ticker provided")

        f.write(data)

    t2 = time()
    print(
        f"Completed fetching ${ticker} data ({t2 - t1:.2f}s)")

    return 1

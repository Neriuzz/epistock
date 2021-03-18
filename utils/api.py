#!usr/bin/env python3

"""
Uses the alpha vantage API to retrieve a large amount of historical
stock price data for a speific marker and saves it to stock_data.csv

Author: Nerius Ilmonas
Date: 15/03/2021
"""


import os
import requests
import time

# Get API key from environment variables and create request URL
API_KEY = os.getenv("ALPHA_VANTAGE_KEY")

# Make sure user has set their API key
if not API_KEY:
    raise Exception("Alpha Vantage API key has not been set!")

BASE_URL = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&"


def get_stock_data(ticker, interval):
    """
    Downloads 2 years and 12 months worth of stock
    price data based on a specific a stock ticker and 
    time interval e.g. AAPL 5mins
    """

    year, month = 1, 1
    url = BASE_URL + \
        f"symbol={ticker}&outputsize=full&datatype=csv&apikey={API_KEY}"

    # Initialise timer
    t1 = time.time()

    print(f"Fetching ${ticker} data...")

    # Initialise .csv file
    with open("stock_data.csv", "w") as f:
        # Write .csv headers
        print("time,open,high,low,close,volume", file=f)

    
    t2 = time.time()
    print(
        f"Completed fetching ${ticker} data ({t2 - t1:.2f}s)")

    return

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

BASE_URL = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY_EXTENDED&"


def get_stock_data(ticker, interval):
    """
    Downloads 2 years and 12 months worth of stock
    price data based on a specific a stock ticker and 
    time interval e.g. AAPL 5mins
    """

    year, month = 1, 1
    url = BASE_URL + \
        f"symbol={ticker}&interval={interval}min&slice=year{year}month{month}&apikey={API_KEY}"

    # Initialise timer
    t1 = time.time()

    print(f"Fetching ${ticker} data...")

    # Initialise .csv file
    with open("stock_data.csv", "w") as f:
        # Write .csv headers
        print("time,open,high,low,close,volume", file=f)

    # Loop through 2 years and 12 months worth of data
    for i in range(2):
        for j in range(12):
            url = url.replace(
                f"year{year}month{month + j - 1}", f"year{year}month{month + j}")

            data = "".join(requests.get(url).text.split("\n")[1:])

            # Data fetched was not valid
            if not data:
                raise Exception("Invalid ticker or interval")

            with open("stock_data.csv", "a") as f:
                f.write(data)

            # Prevent getting rate limited (Can only make 5 requests per minute)
            time.sleep(12.5)

        year += 1
        url = url.replace(f"year{year - 1}month{12}", f"year{year}month{1}")

    t2 = time.time()

    print(
        f"Completed fetching ${ticker} data at {interval}m intervals ({t2 - t1:.2f}s)")

    return

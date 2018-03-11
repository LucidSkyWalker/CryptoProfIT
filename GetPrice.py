import csv
import datetime
import codecs
import time
import math
import requests

BTC_data_line = 0
BTC_data = ""
timestamp = ""

def get_BTC_Price(timestamp, price_data):
        df_sort = price_data.iloc[(price_data[0] - timestamp).abs().argsort()[:1]]
        return price_data[1][df_sort.index.tolist()[0]]

def getPrice(timestamp, token, price_data):
    if token == "ETH":
        return get_ETH_Price(timestamp, price_data)
    if token == "BTC":
        return get_BTC_Price(timestamp, price_data)


def get_ETH_Price(timestamp, price_data):
    # Throttle the requests. Rate limit is 1/sec
    time.sleep(1.1)
    try:
        req = 'https://poloniex.com/public?command=returnChartData&currencyPair=BTC_ETH&start={}&end={}&period=300'
        req = req.format(timestamp, timestamp+300)
        # Make the request
        res = requests.get(req)
        j = res.json()
        if len(j) == 0:
            print ('WARNING: Response was empty.')
            return None
        # Calculate $ Price of ETH From ETH-BTC pair
        BTC_price = float(getPrice(timestamp, "BTC", price_data))
        return ((j[0]['high'] + j[0]['low']) / 2.)*BTC_price
    except:
        # Occasionally, the request will fail. We will just retry.
        return get_ETH_Price(timestamp)
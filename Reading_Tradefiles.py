import csv
import codecs
import GetPrice
import time
import datetime
import pandas as pd
import os
import sys
import logging
from currency_converter import CurrencyConverter

# Fallbacks are used for missing USD data (occurs for some dates)
c = CurrencyConverter(fallback_on_wrong_date=True, fallback_on_missing_rate=True, verbose=False)

# Read BTC Price Data
BTC_data = "./BTC_Data/fixed.hdf5"
try:
    price_data = pd.read_hdf(BTC_data)
except:
    logging.warning("fixed.hdf5 file is missing or corrupt")
    print("It seems like you didn't download the 'fixed.hdf5' file. Please read the HOWTO:\n"
          "https://github.com/LucidSkyWalker/CryptoProfIT/blob/master/README.md")
    input("Press enter to exit")
    sys.exit()

# Getting tradefiles
filelist = os.listdir("./trade_history_files")

# The default source of this API is the European Central Bank
def Get_EUR_USD_exchange_rate(date):
    return c.convert(1, 'EUR', 'USD', date=date)

###################################################
           ######## Binance #######  UTC
###################################################
def Read_Binance():
    print("Reading Binance")
    binance_orders = list()
    trade_counter = 0
    csvReader = csv.reader(codecs.open('./trade_history_files/binance.csv'), delimiter=';')
    # Skip headers
    next(csvReader)
    for row in csvReader:
        trade_counter += 1
        print("\tAnalyzing trade: " + str(trade_counter))
        date = datetime.datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
        row[0] = date.strftime("%Y-%m-%d %H:%M:%S")
        token_cache = row[1].split(row[7])
        if token_cache[0] == "":
            row[1] = row[7]+"-"+token_cache[1]
        if token_cache[1] == "":
            row[1] = token_cache[0]+"-"+row[7]
        split_cache = row[1].split("-")
        if "SELL" == row[2]:
            row[2] = "Sell"
        if "BUY" == row[2]:
            row[2] = "Buy"
        row[3], row[4] = row[4], row[3]
        # SELL Fees for Binance are charged in Pair[1]
        if row[2] == "Sell":
            row[5] = row[6]
            row[6] = row[7]
        # BUY Fes are charged in Pair[0]
        if row[2] == "Buy":
            row[5] = str(float(row[4]) * float(row[5]))
            row[6] = split_cache[0]
        row[7] = "Binance"
        if "BTC" == split_cache[1]:
            row.append(str(GetPrice.getPrice(int(time.mktime(date.timetuple())), "BTC", price_data)))
        elif "ETH" == split_cache[1]:
            row.append(str(GetPrice.getPrice(int(time.mktime(date.timetuple())), "ETH", price_data)))
        elif "USDT" == split_cache[1]:
            row.append(str(1))
        else:
            logging.info("Trades with {} as base are not yet supported. Please contact me, see Readme.txt."
                         .format(split_cache[1]))
            print("Trades with {} as base are not yet supported. Please contact me, see Readme.txt."
                  .format(split_cache[1]))
            sys.exit("Trades with {} as base are not yet supported. Please contact me, see Readme.txt."
                     .format(split_cache[1]))
        binance_orders.append(row)
    return binance_orders


###################################################
           ######## BITTREX #######
###################################################
def Read_Bittrex():
    print("Reading Bittrex")
    bittrex_orders = list()
    csvReader = csv.reader(codecs.open('./trade_history_files/bittrex.csv', 'rU', 'UTF-16LE'), delimiter=',')
    trade_counter = 0
    # Skip headers
    next(csvReader)
    for row in csvReader:
        trade_counter += 1
        print("\tAnalyzing trade: " + str(trade_counter))
        # Bittrex Date in Column 8. Get Date and overwrite in new format.
        date = datetime.datetime.strptime(row[8], "%m/%d/%Y %I:%M:%S %p")
        row[0] = date.strftime("%Y-%m-%d %H:%M:%S")
        split_cache = row[1].split("-")
        # Switch Pair in BITTREX
        row[1] = split_cache[1] + "-" + split_cache[0]
        if "SELL" in row[2]:
            row[2] = "Sell"
        if "BUY" in row[2]:
            row[2] = "Buy"
        # Switch column of price.
        row[4] = str(float(row[6])/float(row[3]))
        row[6] = split_cache[0]
        row[7] = "Bittrex"
        if "BTC" == split_cache[0]:
            row[8] = str(GetPrice.getPrice(int(time.mktime(date.timetuple())), "BTC", price_data))
        elif "ETH" == split_cache[0]:
            row[8] = str(GetPrice.getPrice(int(time.mktime(date.timetuple())), "ETH", price_data))
        elif "USDT" == split_cache[0]:
            row[8] = str(1)
        else:
            logging.info("Trades with {} as base are not yet supported. Please contact me, see Readme.txt."
                         .format(split_cache[1]))
            print("Trades with {} as base are not yet supported. Please contact me, see Readme.txt."
                  .format(split_cache[0]))
            sys.exit("Trades with {} as base are not yet supported. Please contact me, see Readme.txt."
                     .format(split_cache[0]))
        bittrex_orders.append(row)
    return bittrex_orders


###################################################
           ######## Poloniex #######  UTC
###################################################
def Read_Poloniex():
    print("Reading Poloniex")
    poloniex_orders = list()
    csvReader = csv.reader(codecs.open('./trade_history_files/poloniex.csv'), delimiter=',')
    trade_counter = 0
    # Skip headers
    next(csvReader)
    for row in csvReader:
        trade_counter += 1
        print("\tAnalyzing trade: " + str(trade_counter))
        date = datetime.datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
        row[1] = row[1].replace("/", "-")
        split_cache = row[1].split("-")
        row[2] = row[3]
        row[3] = row[5]
        # SELL Fees for Poloniex are in BTC, BUY Fees are charged in the Token you buy..
        if row[2] == "Sell":
            row[5] = str(float(row[7][:-1]) * float(row[9])*0.01)
        # Get FEE and calculate Fee in BTC #  0.XX% * Amount * price * 0.01 (cause of %)
        if row[2] == "Buy":
            row[5] = str(float(row[7][:-1]) * float(row[5]) * float(row[4]) * 0.01)
        row[6] = split_cache[1]
        row[7] = "Poloniex"
        # Get Prices
        if "BTC" in row[1]:
            row[8] = str(GetPrice.getPrice(int(time.mktime(date.timetuple())), "BTC", price_data))
        elif "ETH" in row[1]:
            row[8] = str(GetPrice.getPrice(int(time.mktime(date.timetuple())), "ETH", price_data))
        elif "USDT" == split_cache[1]:
            row[8] = str(1)
        else:
            logging.info("Trades with {} as base are not yet supported. Please contact me, see Readme.txt."
                         .format(split_cache[1]))
            print("Trades with {} as base are not yet supported. Please contact me, see Readme.txt."
                  .format(split_cache[1]))
            sys.exit("Trades with {} as base are not yet supported. Please contact me, see Readme.txt."
                     .format(split_cache[1]))
    poloniex_orders.append(row[:9])
    return poloniex_orders


###################################################
           ######## Kraken #######  UTC
###################################################
def Read_Kraken():
    print("Reading Kraken")
    kraken_orders = list()
    csvReader = csv.reader(codecs.open('./trade_history_files/kraken.csv'), delimiter=',')
    trade_counter = 0
    # Skip headers
    next(csvReader)
    for row in csvReader:
        supported_coins = ["XBT", "EUR", "USD", "ETH", "BCH", "DASH", "EOS", "GNO", "ICN", "LTC", "MLN", "REP"
            , "USDT", "XDG", "XLM", "XMR", "XRP", "ZEC"]
        trade_counter += 1
        print("\tAnalyzing trade: " + str(trade_counter))
        if (row[2][0] == 'X'):
            for coin in supported_coins:
                if coin in row[2]:
                    a = row[2].split(coin)
                    if len(a[0]) > len(a[1]):
                        row[1] = a[0][1:-1] + "-" + coin
                    else:
                        row[1] = coin + "-" + a[1][1:]
        else:
            for coin in supported_coins:
                if coin in row[2]:
                    a = row[2].split(coin)
                    if len(a[0]) > len(a[1]):
                        row[1] = a[0] + "-" + coin
                    else:
                        row[1] = coin + "-" + a[1]
        date = datetime.datetime.strptime(row[3].split(".")[0], "%Y-%m-%d %H:%M:%S")
        row[0] = date.strftime("%Y-%m-%d %H:%M:%S")
        row[1] = row[1].replace("XBT", "BTC")
        split_cache = row[1].split("-")
        row[2] = row[4]
        if "sell" == row[2]:
            row[2] = "Sell"
        if "buy" == row[2]:
            row[2] = "Buy"

        row[3] = row[9]
        row[4] = row[6]
        row[5] = row[8]
        row[6] = split_cache[1]
        row[7] = "Kraken"
        if "BTC" == split_cache[1]:
            row[8] = str(GetPrice.getPrice(int(time.mktime(date.timetuple())), "BTC", price_data))
        elif "ETH" == split_cache[1]:
            row[8] = str(GetPrice.getPrice(int(time.mktime(date.timetuple())), "ETH", price_data))
        elif "EUR" == split_cache[1]:
            row[8] = str(Get_EUR_USD_exchange_rate(date))
        elif "USD" == split_cache[1]:
            row[8] = str(1)
        else:
            logging.info("Trades with {} as base are not yet supported. Please contact me, see Readme.txt."
                         .format(split_cache[1]))
            print("Trades with {} as base are not yet supported. Please contact me, see Readme.txt."
                  .format(split_cache[1]))
            sys.exit("Trades with {} as base are not yet supported. Please contact me, see Readme.txt."
                     .format(split_cache[1]))
        kraken_orders.append(row[:9])
    return kraken_orders


###################################################
           ######## Mercatox #######  UTC
###################################################
def Read_Mercatox():
    print("Reading Mercatox")
    mercatox_orders = list()
    csvReader = csv.reader(codecs.open('./trade_history_files/mercatox.csv'), delimiter=',')
    trade_counter = 0
    print("Note: Mercatox does not export the fees in the CSV file")
    logging.info("Note: Mercatox does not export the fees in the CSV file")
    # Skip headers
    next(csvReader)
    for row in csvReader:
        trade_counter += 1
        print("\tAnalyzing trade: " + str(trade_counter))
        date = datetime.datetime.strptime(row[6], "%b %d, %Y, %I:%M:%S %p")
        row[0] = date.strftime("%Y-%m-%d %H:%M:%S")
        price_cache = row[1]
        row[1] = row[4].replace('/', '-')
        split_cache = row[1].split("-")
        row[3] = row[2]
        if "sell" == row[5]:
            row[2] = "Sell"
        if "buy" == row[5]:
            row[2] = "Buy"
        row[4] = price_cache
        # Todo: mercatox fees
        row[5] = "0"
        row[6] = split_cache[1]
        row.append("Mercatox")
        if "BTC" in row[1]:
            row.append(str(GetPrice.getPrice(int(time.mktime(date.timetuple())), "BTC", price_data)))
        elif "ETH" in row[1]:
            row.append(str(GetPrice.getPrice(int(time.mktime(date.timetuple())), "ETH", price_data)))
        elif "EUR" == split_cache[1]:
            row[8] = str(Get_EUR_USD_exchange_rate(date))
        elif "USD" == split_cache[1]:
            row[8] = str(1)
        else:
            logging.info("Trades with {} as base are not yet supported. Please contact me, see Readme.txt."
                         .format(split_cache[1]))
            print("Trades with {} as base are not yet supported. Please contact me, see Readme.txt."
                  .format(split_cache[1]))
            sys.exit("Trades with {} as base are not yet supported. Please contact me, see Readme.txt."
                     .format(split_cache[1]))
        mercatox_orders.append(row)
    return mercatox_orders

###################################################
           ######## Bitfinex #######
###################################################
def Read_Bitfinex():
    print("Reading Bitfinex")
    bitfinex_orders = list()
    csvReader = csv.reader(codecs.open('./trade_history_files/bitfinex.csv'), delimiter=',')
    trade_counter = 0
    # Skip headers
    next(csvReader)
    for row in csvReader:
        trade_counter += 1
        print("\tAnalyzing trade: " + str(trade_counter))
        date = datetime.datetime.strptime(row[6], "%Y-%m-%d %H:%M:%S")
        row[0] = row[6]
        split_cache = row[1].split("/")
        row[1] = row[1].replace('/', '-')
        price_cache = row[3]
        row[3] = abs(float(row[2]))
        if "-" in row[2]:
            row[2] = "Sell"
        else:
            row[2] = "Buy"
        row[4] = price_cache
        # Calculating Fees relative to BasePair
        if row[6] == split_cache[1]:
            row[5] = abs(float(row[6]))
        if row[6] == split_cache[0]:
            row[5] = abs(float(row[4]) * float(row[5]))
        row[6] = split_cache[1]
        row.append("Bitfinex")
        if "BTC" in row[1]:
            row.append(str(GetPrice.getPrice(int(time.mktime(date.timetuple())), "BTC", price_data)))
        elif "ETH" in row[1]:
            row.append(str(GetPrice.getPrice(int(time.mktime(date.timetuple())), "ETH", price_data)))
        elif "EUR" == split_cache[1]:
            row[8] = str(Get_EUR_USD_exchange_rate(date))
        elif "USD" == split_cache[1]:
            row[8] = str(1)
        else:
            logging.info("Trades with {} as base are not yet supported. Please contact me, see Readme.txt."
                         .format(split_cache[1]))
            print("Trades with {} as base are not yet supported. Please contact me, see Readme.txt."
                  .format(split_cache[1]))
            sys.exit("Trades with {} as base are not yet supported. Please contact me, see Readme.txt."
                     .format(split_cache[1]))
        bitfinex_orders.append(row)
    return bitfinex_orders


###################################################
    ######## Dummy file #######  UTC
###################################################
def Read_Dummy():
    print("Reading Dummy")
    dummy_orders = list()
    csvReader = csv.reader(codecs.open('./trade_history_files/dummy.csv'), delimiter=';')
    trade_counter = 0
    # Skip headers
    next(csvReader)
    for row in csvReader:
        trade_counter += 1
        print("\tAnalyzing trade: " + str(trade_counter))
        date = datetime.datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
        row[0] = date.strftime("%Y-%m-%d %H:%M:%S")
        split_cache = row[1].split("-")  # Pairs
        if "SELL" == row[2]:
            row[2] = "Sell"
        if "BUY" == row[2]:
            row[2] = "Buy"
        row[3], row[4] = row[4], row[3]
        # 0, if no fees were noted
        if row[5] == "":
            row[5] = 0
        row.append("Dummy")
        if "BTC" == split_cache[1]:
            row.append(str(GetPrice.getPrice(int(time.mktime(date.timetuple())), "BTC", price_data)))
        elif "ETH" == split_cache[1]:
            row.append(str(GetPrice.getPrice(int(time.mktime(date.timetuple())), "ETH", price_data)))
        elif "EUR" == split_cache[1]:
            row.append(str(Get_EUR_USD_exchange_rate(date)))
        elif "USD" == split_cache[1]:
            row.append(str(1))
        elif "USDT" == split_cache[1]:
            row.append(str(1))
        else:
            logging.info("Trades with {} as base are not yet supported. Please contact me, see Readme.txt."
                         .format(split_cache[1]))
            print("Trades with {} as base are not yet supported. Please contact me, see Readme.txt."
                  .format(split_cache[1]))
            sys.exit("Trades with {} as base are not yet supported. Please contact me, see Readme.txt."
                     .format(split_cache[1]))
        dummy_orders.append(row)
    return dummy_orders

def create_full_tradehistory():
    # List for collecting trade histories
    all_orders = list()

    # Collecting&formatting trade histories
    if "dummy.csv" in filelist:
        logging.info('Reading Dummy')
        try:
            dummy_order = Read_Dummy()
        except:
            logging.warning('Something is wrong with your dummy file. Please check the formats!')
            print("Something is wrong with your dummy file. Please check the formats!"
                  "\n(e.g. datetime format needs to be Y-m-d H:M:S, and decimal number need '.')")
            input("Press ENTER to ABORT")
            sys.exit("Format Error in Dummy-File")
        all_orders += dummy_order
    if "kraken.csv" in filelist:
        logging.info('Reading Kraken')
        kraken_order = Read_Kraken()
        all_orders += kraken_order
    if "bittrex.csv" in filelist:
        logging.info('Reading Bittrex')
        bittrex_order = Read_Bittrex()
        all_orders += bittrex_order
    if "poloniex.csv" in filelist:
        logging.info('Reading Poloniex')
        poloniex_order = Read_Poloniex()
        all_orders += poloniex_order
    if "binance.csv" in filelist:
        logging.info('Reading Binance')
        binance_order = Read_Binance()
        all_orders += binance_order
    if "mercatox.csv" in filelist:
        logging.info('Reading Mercatox')
        mercatox_order = Read_Mercatox()
        all_orders += mercatox_order
    if "bitfinex.csv" in filelist:
        logging.info('Reading Bitfinex')
        bitfinex_order = Read_Bitfinex()
        all_orders += bitfinex_order

    # Sorting trades
    market_orders = sorted(list(all_orders), key=lambda o: datetime.datetime.strptime(o[0], "%Y-%m-%d %H:%M:%S"))
    return market_orders

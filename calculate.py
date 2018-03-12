import csv
import datetime
import Reading_Tradefiles
from collections import defaultdict
import logging
import sys

# Dictionary for Coins
coins = defaultdict()
# Gains
profit = 0.0
profit_list = list()
# Overall payed Fees
fee_costs_overall = 0

# Create holding output
date = datetime.datetime.now().strftime("%Y-%m-%d_%H_%M")
output_h_file = "holding_output.csv"


# Buy Transaction
# Type: Sell/Buy, pair e.g. ETH-BTC, Amount1 is bought, Amount2 is sold, price of pair[0] relative to base price (pair[1])
def transaction(type, pair, amount1, amount2, timestamp, price, base_price, fiat_of_profit, date, exchange):
    global profit
    this_full_profit = 0
    # This part ADDS new entries to the coins dict.
    if type == "Buy":
        if pair[0] in coins:
            coins[pair[0]].append(
                {"amount": float(amount1), "price": float(base_price) * float(price), "timestamp": timestamp})
        else:
            coins[pair[0]] = [
                {"amount": float(amount1), "price": float(base_price) * float(price), "timestamp": timestamp}]
        # For calculating the Profit in Buy Orders the Base price is used:
        price = base_price
    if type == "Sell":
        if pair[0] in coins:
            coins[pair[0]].append(
                {"amount": float(amount1), "price": float(base_price), "timestamp": timestamp})
        else:
            coins[pair[0]] = [{"amount": float(amount1), "price": float(base_price), "timestamp": timestamp}]
        # For calculating the Profit in Sell Orders the TokenPrice is used --> price*base_price
        price = float(price) * float(base_price)

    # Check if second token of the pair is in coin dict

    if pair[1] not in coins:
        coins[pair[1]] = []

    # This code block Reduces/DELETES entries of the coins dict.
    amount_to_delete = float(amount2)
    # If EUR were payed ....
    if pair[1] == "EUR" or pair[1] == "USD":
        coins[pair[1]].append({"amount": -amount_to_delete, "timestamp": timestamp})
    # If token to token
    else:
        # FIFO: The sold tokens are taken from the beginning. coins[pair[1][0]] indicates the first entry.
        for i in range(len(coins[pair[1]])):
            if amount_to_delete == 0:
                break
            if coins[pair[1]][0]["amount"] <= amount_to_delete:
                # Profit -> pricedifference * amount
                amount_to_delete = amount_to_delete - coins[pair[1]][0]["amount"]
                this_profit = (float(price) - float(coins[pair[1]][0]["price"])) * coins[pair[1]][0]["amount"]
                if fiat_of_profit == "EUR":
                    this_profit /= Reading_Tradefiles.Get_EUR_USD_exchange_rate(date)
                profit += this_profit
                this_full_profit += this_profit
                del coins[pair[1]][0]
            else:
                coins[pair[1]][0]["amount"] = coins[pair[1]][0]["amount"] - amount_to_delete
                # Profit -> pricedifference * amount
                this_profit = (float(price) - coins[pair[1]][0]["price"]) * amount_to_delete
                if fiat_of_profit == "EUR":
                    this_profit /= Reading_Tradefiles.Get_EUR_USD_exchange_rate(date)
                profit += this_profit
                this_full_profit += this_profit
                amount_to_delete = 0
        if amount_to_delete != 0:
            logging.warning(
                "You sold {} {} on {} ({}), but you didnt have enough (deviation = {}). "
                "\nYour tradehistory seems to be is incomplete. If this transaction involves a forked coin,"
                "\nyou need add the receiving date for proper profit calculation, see ReadMe.txt"
                    .format(amount2, pair[1], date, exchange, amount_to_delete))
            print("WARNING: You sold {} {} on {} ({}), but you didnt have enough (deviation = {}). "
                  "\nYour tradehistory seems to be is incomplete. If this transaction involves a forked coin,"
                  "\nyou need add the receiving date for proper profit calculation, see ReadMe.txt"
                  .format(amount2, pair[1], date, exchange, amount_to_delete))
            a = input("Press 'c' to continue, any other key to abort...")
            if a != 'c':
                logging.info("User aborted due to a inaccurate trade history")
                sys.exit("Aborted")
    # New Profit - Old Profit = Profit of this transaction
    profit_list.append(round(this_full_profit, 2))


def calculate_all_trades(market_order, fiat_of_profit):
    global fee_costs_overall
    for row in market_order:
        # TODO: Add other rebrandings
        row = [w.replace("ANS", "NEO") if isinstance(w, str) else w for w in row]
        pair = row[1].split("-")
        if (row[2] == "Buy"):
            transaction(row[2], pair, float(row[3]), float(row[3]) * float(row[4])
                        , row[0], row[4], row[8], fiat_of_profit
                        , datetime.datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S"), row[7])

        if (row[2] == "Sell"):
            pair[0], pair[1] = pair[1], pair[0]
            transaction(row[2], pair, float(row[3]) * float(row[4]), float(row[3])
                        , row[0], row[4], row[8], fiat_of_profit
                        , datetime.datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S"), row[7])

        # Calculate Fees:
        if row[6]:
            this_fee_cost = float(row[5]) * float(row[8])
            fee_costs_overall += this_fee_cost


def get_results(market_orders, fiat_of_profit):
    print("Calculating results...")
    calculate_all_trades(market_orders, fiat_of_profit)
    with open(output_h_file, 'w') as output:
        wr = csv.writer(output, lineterminator='\n')
        wr.writerow(["Payed Fees: " + str(round(fee_costs_overall, 2)) + fiat_of_profit])
        wr.writerow(["Your Profit: " + str(round(profit, 2)) + fiat_of_profit])
        wr.writerow([""])
        wr.writerow(["Your Assets: "])
        wr.writerow(["Explanation: "])
        wr.writerow(["{'amount': quantity of Assets, 'price': price per Asset in USD, 'timestamp': Buy date}"])
        wr.writerow([""])
        for key in coins:
            total_amount = 0
            value = 0
            has_value = False
            # Skip empty lists
            if not coins[key]:
                continue
            for entry in coins[key]:
                total_amount += entry["amount"]
                if "price" in entry:
                    value += entry["price"] * entry["amount"]
                    has_value = True
            # Skip "dust" coins
            if has_value and value < 1:
                continue
            wr.writerow([key + ": " + str(coins[key])])
            wr.writerow([key + ": Total Amount = " + str(round(total_amount, 2))])
            print(key + ": Total Amount = " + str(round(total_amount, 2)))

        print("*****************************************************")
        print("Payed Fees: " + str(round(fee_costs_overall, 2)) + " " + fiat_of_profit)
        print("Overall Profit: " + str(round(profit, 2)) + " " + fiat_of_profit)
        print("*****************************************************")
        print("Detailed Output: " + output_h_file)
        print("Successfully finished\n\n")
        return profit_list


def fiat_of_profit():
    print("Choose your fiat for the profit calculation:")
    fiat = input("Type 'a' for EURO and 'b' for USD\n")
    if fiat == "a":
        return "EUR"
    if fiat == "b":
        return "USD"
    else:
        return fiat_of_profit()

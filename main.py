import csv
import Reading_Tradefiles
import datetime
import calculate
import logging

# Gets User input for definition of fiat currency.
fiat_of_profit = calculate.fiat_of_profit()
# Initialize Logfile
date = datetime.datetime.now().strftime("%Y-%m-%d_%H_%M")
logging.basicConfig(filename='info__{}.log'.format(date), level=logging.INFO)
logging.info('Started')
# Path for outputfile
output_file = "output__{}.csv".format(date)

print("\n**************************************************")
print("DISCLAIMER:")
print("It is not guaranteed that the results are correct.")
print("Use the output files to verify the results.")
print("**************************************************\n")

market_orders = Reading_Tradefiles.create_full_tradehistory()
# Calculate results and write new output file

profit_list = calculate.get_results(market_orders, fiat_of_profit)

with open(output_file, 'w') as output:
    wr = csv.writer(output, lineterminator='\n', delimiter=';')
    wr.writerow(['Date', 'Pair', 'Type', 'Amount', 'Price', 'Fee', 'Fee Coin',
                 'Exchange', 'Base Price in USD', 'Profit in {}'.format(fiat_of_profit)])
    if len(market_orders) != len(profit_list):
        print("Error in Profit list... be careful")
    for i in range(len(market_orders)):
        if fiat_of_profit == "USD":
            # US EXCEL uses "." for displaying decimals
            row = [str(o).replace(",", ".") for o in market_orders[i]]
            row.append(str(profit_list[i]).replace(".", ",")+" USD")
        if fiat_of_profit == "EUR":
            # German EXCEL uses "," for displaying decimals
            row = [str(o).replace(".", ",") for o in market_orders[i]]
            # Profit USD / Exchangerate = Profit EUR. market_orders[i][0] -> gets the date of this profit
            row.append(str((round(profit_list[i]/Reading_Tradefiles
                           .Get_EUR_USD_exchange_rate(datetime.datetime
                                                      .strptime(market_orders[i][0]
                                                                , "%Y-%m-%d %H:%M:%S")), 2))).replace(".",","))
        wr.writerow(row)
    # Last line. Sum of all Profits
    wr.writerow(['', '', '', '', '', '', '',
                 '', '', '{}'.format(str(round(sum(profit_list),2))).replace(".",",")])
print("Full Trade History saved to: " + output_file + "\n")
print("XRB TO THE MOON!")
print("Donations: xrb_3mwnrhq1d4pdcrgegyygic1a1wpcbnsaj6pd5656dg3yxio3cyg1rn4u1umx")









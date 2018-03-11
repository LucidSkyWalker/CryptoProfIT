# CryptoProfIT (Alpha Version)
Free Python Script to process your trade histories. The profit result can be used for Taxes.

The output are two csv-files. Example Screenshots can be found below.  
The output files contain: 
- Sorted full trade history (converts all exchange exports to the same formatting)
- Fees per Trade (inklusive Overall Payed fees)
- Profit per trade (Overall profit. This can be used to easily calculate your personal capital taxes)
- Profit can be calculated in EUR or USD. (Data from European Central Bank)
- Amount of your Cryptocurrencies
- Display the different BUY-INs by amount and date. So you can control the 12 month holding period.


Supported Exchanges: Binance, Bitfinex, Bittrex, Kraken, Mercatox, Poloniex, Costum*

\*A dummy file is included that can be used to easily add trades of other exchanges.<br />
If you give me a csv-file export from other exchanges (you can modify the digits for privacy) I will add them.

## Requirements
For now, there is no Gui so you have to use the python script.<br />
If some dev likes to help, making a gui or a brython version would be neat.

### HOWTO:
Setting up Python:
* Install Python 3.x [(link here)](https://www.python.org/downloads/)
* Make sure to mark "ADD PATH" in the installer
* Open commandline
* Type: "python --version", this should display "Python 3.x"
* Install package: "requests" (type: "pip3 install requests", hit ENTER) (if applicable, run commandline as admin)
* Install package: "pandas" (type: "pip3 install pandas", hit ENTER)
* Install package: "currencyconverter" (type: "pip3 install currencyconverter", hit ENTER)*
* Install package: "tables" (type: "pip3 install tables", hit ENTER)

Using the script:
* Download the csv-file exports and copy them into the folder "trade_history_files"   
Note: Binance will give you an excel file. Export this file as a csv
* Rename the csv-files into the exchange names with lowercase. E.g. "kraken.csv", "binance.csv"...
* For further trades, copy the "dummy.csv" file from the "costum folder" into "trade_history_files".   
(See section "Using a costum file". I used it for Anycoin and Liqui, as I could not get csv files there) 
* Start the "main.py"  
(Detailed: navigate via commandline into the "CryptoTaxator" folder  
e.g type: "cd C:/CryptoTaxator", hit Enter, type: "Python3 main.py")
* If you choose EUR, decimals in the output will be seperated with ",", for USD with "." (For proper Excel display)
* Forks are displayed with a warning, as you try to sell tokens you never bought before.   Please read the Fork information if your trade history contains forks.


\* This package uses the European Central Bank as source for EUR/USD to get the historical exchange rates.  
Author: Alex Prengère   
Home Page: https://github.com/alexprengere/currencyconverter

### Fork information:
A tax accountant told me, you need to pay taxes on the profit of your received coins as soon as you get them.  
Therefore a "fake" trade needs to be manually added to one of the csv export files in "trade_history_files".  
* Add a "Buy" transaction at the moment you reveived the coins. (with price "0")   
* Add a "Sell" transaction a few seconds later (price = initial price of forked coin) --> you made the inital profit.  
* Add a "Buy" transaction a few seconds later than before (price = initial price) --> Because you know still got the coins   
Simplifing this could be a feature in a future version...



## Contact
If you run into any problems, don't hesitate to contact me at any time. 


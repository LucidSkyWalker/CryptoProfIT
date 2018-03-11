# CryptoProfIT (Alpha Version)   
<img align="right" src="https://user-images.githubusercontent.com/19948182/37255611-f5497340-254e-11e8-93a4-43fe296e20b2.png" width="150">
Free Python Script to process your trade histories.<br /> The profit result can be used to calculate the tax on your crypto.<br /><br />
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
If you give me a csv-file export from other exchanges (you can modify the digits for privacy) I will add them.<br /><br />
**PLEASE READ**: I wrote this tool to calculate my taxes and it did the job fine! Nevertheless it is not well tested yet. <br />If you run into trouble, please write an issue and I will fix it! Thank you :)

## Screenshots
Screenshot of the output.csv. The data of all exchanges is formatted in its specific ways and displayed in a uniform style.<br /> **Type** always refers to the first token of the pair! (First transaction shows buying XRP by BTC)<br /> **Base Price** always refers to the second token of the pair.<br />**Base Price in USD** shows the price of the second token in USD.<br /><br />
<img src="https://user-images.githubusercontent.com/19948182/37256193-9a14af4a-2557-11e8-9844-2d3045653609.png" width="700"><br /><br />
Screenshot of the holding_output.csv. This file can be used to specify your remaining holding times,<br />
as Capital gains do not need to be taxed in many countries after 12 month<br />
The picture shows (in red), that the first of the remaining ETH were bought on 2017-06-02, meaning that this amount is tax-free one year later.<br />
The blue frame shows the date for the next tokens...<br /><br />
<img src="https://user-images.githubusercontent.com/19948182/37256327-48d9386a-2559-11e8-9798-2d31e0ecc703.png" width="700"><br /><br />

Console output of the Python script (Not my real data ;) <br /><br />
<img src="https://user-images.githubusercontent.com/19948182/37256205-bd9a468c-2557-11e8-9853-90d2f1daaa08.png" width="700"><br /><br />


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
* Download or clone this git
* Download the historical price data file (https://github.com/LucidSkyWalker/CryptoProfIT/raw/master/BTC_Data/fixed.hdf5)
* Copy the file into the BTC_Data folder and overwrite existing fixed.hdf5
* Download the csv-file exports and copy them into the folder "trade_history_files"   
Note: Binance will give you an excel file. Open that and save it as binance.csv  
Note: For Kraken, use "trade" (not ledger) and mark "all"
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
A tax accountant told me, you need to pay taxes on the profit of your received forked coins as soon as you get them.  
Therefore a "dummy" trade needs to be manually added to one of the csv export files in "trade_history_files".  
* Add a "Buy" transaction at the moment you reveived the coins. (with price "0")   
* Add a "Sell" transaction a few seconds later (price = initial price of forked coin) --> you made the inital profit.  
* Add a "Buy" transaction a few seconds later than before (price = initial price) --> Because you know still got the coins   
Simplifing this could be a feature in a future version...

### Using the dummy-file:
You can use this file to add trades from exchanges that do not provide trade history exports.<br />
**Important:** You have to use the same formatting like the sample data in the file.<br />
Ensure the right date formatting, and use "." for decimals.

### Other Information:

* For receiving the minute price data of bitcoin, the historical data of coinbase is used.
* For receiving the ETH price data, the poloniex API is used ( ~ 5min accuracy )
* For the USD/EUR exchange rate, the european central bank data is used.
* If you try to sell something you should not have it is displayed in the console. You can choose to continue or abort. If you sell a coin you received from a fork, this message will show up as you should not have that coin. Read "Fork information" for more info. 

### Disclaimer:

I wrote this tool to calculate my taxes and thought I share it.<br />
I do not guarantee that the results are 100% accurate, but the script might help you<br />
getting a well formatted output csv you can work with.


## Contact
If you run into any problems, don't hesitate to contact me at any time. <br /><br />

XBR TO THE MOON<br />
Donations: xrb_3mwnrhq1d4pdcrgegyygic1a1wpcbnsaj6pd5656dg3yxio3cyg1rn4u1umx


# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 18:51:05 2023

@author: Alexander-NB
"""

import pandas as pd
import yfinance as yf


insiders = pd.read_csv("chosen_companies.csv")
ticker = insiders.iloc[:,3]
purchase_price = insiders.iloc[:,8]
purchase_value = insiders.iloc[:, 12]

# Remove the dollar sign and plus/minus sign from the purchase value column
insiders[purchase_value] = insiders[purchase_value].str.replace('$', '')
insiders[purchase_value] = insiders[purchase_value].str.replace('+', '')
insiders[purchase_value] = insiders[purchase_value].str.replace('-', '')

# Convert the purchase value column to float
insiders['purchase_value'] = insiders['purchase_value'].astype(float)

import yfinance as yf
import pandas as pd

# Create an empty portfolio dataframe

portfolio =  pd.read_csv("chosen_companies.csv")

# Sum the purchase value for each ticker
insiders_sum = insiders.groupby(ticker)["Value"].sum().reset_index()
print(insiders_sum)
# Add the purchase price and latest closing price to the portfolio
for ticker in insiders_sum['Ticker']:
    # Get the latest closing price
    stock_info = yf.Ticker(ticker)
    latest_closing_price = stock_info.info['regularMarketPrice']
    purchase_value = insiders_sum.loc[insiders_sum['ticker'] == ticker, 'purchase_value'].item()
    purchase_price = insiders.loc[insiders['ticker'] == ticker, 'purchase_price'].mean()
    performance = (latest_closing_price - purchase_price) / purchase_price
    portfolio = portfolio.append({'ticker': ticker, 'purchase_price': purchase_price, 'purchase_value': purchase_value,'latest_closing_price':latest_closing_price,'performance':performance}, ignore_index=True)


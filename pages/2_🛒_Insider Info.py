#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  2 20:00:45 2023

@author: marvinsilvafortes
"""

import streamlit as st
import yfinance as yf
import pandas as pd



# Get stock data from yfinance
def get_stock_data(ticker, period):
  stock_data = yf.Ticker(ticker).history(period=period)
  return stock_data

# Create a main function
def main():
  # Create a page called "Favourite Stocks"
  st.sidebar.title("Stock Picker")
  st.sidebar.text("Enter a ticker symbol to select a stock:")
  ticker_symbol = st.sidebar.text_input("Ticker symbol")
  st.sidebar.text("Select a period for the stock data:")
  period_options = ["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"]
  period = st.sidebar.selectbox("Period", period_options)


  # Display stock chart and data
  if ticker_symbol:
    st.title(str.upper(ticker_symbol) + " - Stock Data")
    stock_data = get_stock_data(ticker_symbol, period)
    if "Date" in stock_data.columns:
      stock_data.reset_index(inplace=True)    
      stock_data.set_index("Date", inplace=True, date_format="YYYY-MM-DD")
    st.line_chart(stock_data["Close"])
    stock_data_table = stock_data[["Close"]]
    stock_data_table.rename(columns={"Close": "Closing Price"}, inplace=True)
    st.dataframe(stock_data_table)

    # Create an Excel file with the data displayed in the dataframe
    if st.button("Create Excel file"):
      file_name = f"{ticker_symbol}_{period}.xlsx"
      stock_data_table.to_excel(file_name)
      st.success(f"Excel file '{file_name}' created successfully.")
      
    selected_stock = str.upper(ticker_symbol)
    stock_data = yf.Ticker(selected_stock)


    insider_trading_data = pd.read_csv("/Users/marvinsilvafortes/Desktop/7. Semester/Econ mit Python x/Project/pages/InsiderTradesScrapeCSV.csv")
    insider_trading_data["Date"] = pd.to_datetime(insider_trading_data["Date"], format="%b %d", infer_datetime_format=True, dayfirst=True)
    

    # Select the rows where the "ticker" column is equal to "aapl"
    tempdf = insider_trading_data.loc[insider_trading_data['Ticker'] == str.upper(ticker_symbol)]

    st.dataframe(tempdf)



if __name__ == "__main__":
  main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 21 16:13:51 2023

@author: marvinsilvafortes
"""

import pandas as pd
import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
#import seaborn as sns

st.sidebar.title("Stock Filter")
companies_input = st.sidebar.text_input("Enter a comma-separated list of company tickers:", "")
companies_input = companies_input.replace(" ", "")
companies = companies_input.split(",")

# Function for translating tickers into names: 


#def get_company_name(ticker):
#    company_info = yf.Ticker(ticker).info
#    name = company_info["longName"]
#    return name

#print(yf.Ticker(companies_input).info["longName"])
#print(companies_input)

# =============================================================================
# Text Section
# =============================================================================

st.title("1000 Most Recent Insider Trades")
st.markdown("This Table contains the most recent SEC filings for insider Trading Buys & Sells")
st.markdown("Option exercises are not considered")

with st.sidebar.expander("All Companies"): 
    Stocklist = pd.read_excel("Stocklist.xlsx")
    StocksnTickers = Stocklist.iloc[1:, [0,1]]
    StocksnTickers.columns = ['Ticker', 'Company Name']
    
    search_term = st.sidebar.text_input("Ticker or Company Name Search")
    
    filtered_df = StocksnTickers[(StocksnTickers['Company Name'].str.contains(search_term, case=False, na=False)) | (StocksnTickers['Ticker'].str.contains(search_term, case=False, na=False))]
    st.dataframe(filtered_df)

# =============================================================================

# Filter Box: 
if companies_input:
    st.success("Stock Filter for: " + companies_input.upper())
#    st.markdown(get_company_name(companies_input))
else:
    st.warning("Enter a comma-separated list of company tickers to filter")
    
tab1, tab2 = st.tabs(["Table", "Chart"])

# Scraping & Implementation:
insider = pd.DataFrame()
for company in companies: 
    url = f'http://openinsider.com/screener?s={company}&o=&pl=&ph=&ll=&lh=&fd=1461&fdr=&td=0&tdr=&fdlyl=&fdlyh=&daysago=&xp=1&xs=1&vl=&vh=&ocl=&och=&sic1=-1&sicl=100&sich=9999&grp=0&nfl=&nfh=&nil=&nih=&nol=&noh=&v2l=&v2h=&oc2l=&oc2h=&sortcol=0&cnt=1000&page=1'

    insider1 = pd.read_html(url)
    try:
        insider1 = insider1[-3]
        insider = pd.concat([insider, insider1])
        insider = insider.drop(columns=["X", "1d", "1w", "1m", "6m"])
        
        insider = insider.reset_index(drop=True)        
        with tab1:
            st.table(insider)
    except KeyError:
        st.warning("Entered Ticker Filter <" + company.upper() +"> is Invalid or does not exist")

insider.to_csv("chosen_companies.csv")

with tab2: 
    st.markdown("Stock Chart from filtered Stock:")  
    def get_stock_data(ticker, period):
        stock_data = yf.Ticker(ticker).history(period=period)
        return stock_data


    ticker_symbol = company


    # Display stock chart and data
    if ticker_symbol:
      st.header(str.upper(ticker_symbol) + " - Stock Data - 4y")
      stock_data = get_stock_data(ticker_symbol, "4y")
      if "Date" in stock_data.columns:
        stock_data.reset_index(inplace=True)    
        stock_data.set_index("Date", inplace=True, date_format="YYYY-MM-DD")
#    st.line_chart(stock_data['Close'])

    # Add vertical line at 2021-01-01
#    st.add_rows(st.line_chart(stock_data.iloc["2021-01-01" : "2021-01-01", "Close"]))


                  
                
#    insider.plot(x=insider.iloc[:,1], y=insider.iloc[:,7])

    #print(insider[insider.iloc[:,6].str.contains("Purchase")])
    purchase_df = insider[insider.iloc[:,6].str.contains("Purchase")]
    sale_df = insider[insider.iloc[:,6].str.contains("Sale")]

    #print(purchase_df)

   # Matplotlib Method
    # Get stock data for a specific ticker
    ticker = "TSLA"
    stock_data = yf.download(ticker, interval="1d", period="4y")
    
    purchase_df_ticker = purchase_df[purchase_df.iloc[:,2].str.contains(ticker)]
    sale_df_ticker = sale_df[sale_df.iloc[:,2].str.contains(ticker)]

    print(purchase_df_ticker)
    st.header("Table with Insider-Purchases")
    st.table(purchase_df_ticker)
    
    print(sale_df_ticker)
    st.header("Table with Insider-Sales:")
    st.table(sale_df_ticker)

    
    insider.iloc[:,1] = pd.to_datetime(insider.iloc[:,1])
    
    # Plot the "Close" price over time
    plt.plot(stock_data['Close'], color="k")
    plt.xlabel('Date')
    plt.ylabel('Price in $')
    plt.title(f'{ticker} Price')
    plt.xticks(rotation=45)
    
    #print(purchase_df_ticker)

    for index, row in purchase_df_ticker.iterrows():
        date = pd.to_datetime(row[1])
        plt.axvline(x=date, color='g', linestyle='dotted')

    for index, row in sale_df_ticker.iterrows():
        date = pd.to_datetime(row[1])
        plt.axvline(x=date, color='r', linestyle='dotted')

    plt.show()




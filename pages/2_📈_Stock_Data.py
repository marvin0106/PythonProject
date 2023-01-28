#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  1 22:41:42 2023

@author: marvinsilvafortes
"""
import streamlit as st
import yfinance as yf
import pandas as pd


st.set_page_config(
    page_title="InsidersInvest • Stock Data",
    page_icon="📈",
    layout="wide")

# Get stock data from yfinance
def get_stock_data(ticker, period):
  stock_data = yf.Ticker(ticker).history(period=period)
  return stock_data

# Create a main function
def main():
  # Create a page called "Favourite Stocks"
  st.sidebar.title("Stock Picker")
  st.sidebar.text("Enter a ticker symbol to select a stock:")
  ticker_symbol = st.sidebar.text_input("Ticker symbol", value = "AAPL")
  st.sidebar.text("Select a period for the stock data:")
  period_options = ["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"]

  period = st.sidebar.selectbox("Period", period_options, index=5)
  
  
  with st.sidebar: 
      st.sidebar.title("Stock Search")
      Stocklist = pd.read_excel("Stocklist.xlsx")
      StocksnTickers = Stocklist.iloc[1:, [0,1]]
      StocksnTickers.columns = ['Ticker', 'Company Name']
      
      search_term = st.sidebar.text_input("Ticker or Company Name Search")
      
      filtered_df = StocksnTickers[(StocksnTickers['Company Name'].str.contains(search_term, case=False, na=False)) | (StocksnTickers['Ticker'].str.contains(search_term, case=False, na=False))]
      st.dataframe(filtered_df)

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
    #st.markdown(yf.Ticker(ticker_symbol).info["52WeekChange"])
    
    with st.expander("Open to see Stock Data on Closing Price per Date "): 
        st.dataframe(stock_data_table)
        # Create an Excel file with the data displayed in the dataframe
        if st.button("Create Excel file"):
          file_name = f"{ticker_symbol}_{period}.xlsx"
          stock_data_table.to_excel(file_name)
          st.success(f"Excel file '{file_name}' created successfully.")
          
          
    # ======== MAJOR STAKEHOLDERS; EVTL COLUMN ANPASSEN; ICH BEKOMMS NICHT HIN
    stakeholders = pd.DataFrame()
    stakeholders = pd.DataFrame(stakeholders, columns = ['Stakeholder', 'Data'])
    stakeholders = yf.Ticker(ticker_symbol).major_holders
    #stakeholders_df = pd.DataFrame(columns = ['Stakeholder', 'Data'])
    st.dataframe(stakeholders)
    
    
    # ======== NEWS TICKER; WOLLTE LINKS CLICKABLE MACHEN, Geht nicht als Table
    st.header(f"Recent Headlines associated with {ticker_symbol.upper()}")
    News = yf.Ticker(ticker_symbol).news
    news_df = pd.DataFrame.from_records(News)    
    news_df = news_df[['title', 'publisher', 'link',]]
    news_df = news_df.rename(columns={'title': 'Title', 'publisher': 'Publisher', 'link': 'Link'})
    # def make_clickable(link):
    #     # target _blank to open new window
    #     # extract clickable text to display for your link
    #     text = link.split('=')[1]
    #     return f'<a target="_blank" href="{link}">{text}</a>'
    
    # news_df.iloc[:,2] = news_df.iloc[:,2].apply(make_clickable)
    # news_df = news_df.to_html(escape=False)
    # st.write(news_df, unsafe_allow_html=True)
    
    #st.table(news_df.to_html(index=False))    
    
    st.table(news_df)
    
    
    # Create an Excel file with the data displayed in the dataframe
      
    selected_stock = str.upper(ticker_symbol)
    stock_data = yf.Ticker(selected_stock)
    
# =============================================================================
#     #additional information feature in sidebar
#     
# =============================================================================

    st.sidebar.subheader("""Display Additional Information""")
    #checkbox to display stock actions for the searched ticker
    actions = st.sidebar.checkbox("Stock Actions")
    if actions:
        st.subheader("""Stock **actions** for """ + selected_stock)
        display_action = (stock_data.actions)
        if display_action.empty == True:
            st.write("No data available at the moment")
        else:
            st.write(display_action)
    
    #checkbox to display quarterly financials for the searched ticker
    financials = st.sidebar.checkbox("Quarterly Financials")
    if financials:
        st.subheader("""**Quarterly financials** for """ + selected_stock)
        display_financials = (stock_data.quarterly_financials)
        if display_financials.empty == True:
            st.write("No data available at the moment")
        else:
            st.write(display_financials)
    
    #checkbox to display list of institutional shareholders for searched ticker
    major_shareholders = st.sidebar.checkbox("Institutional Shareholders")
    if major_shareholders:
        st.subheader("""**Institutional investors** for """ + selected_stock)
        display_shareholders = (stock_data.institutional_holders)
        if display_shareholders.empty == True:
            st.write("No data available at the moment")
        else:
            st.write(display_shareholders)
    
    #checkbox to display quarterly balance sheet for searched ticker
    balance_sheet = st.sidebar.checkbox("Quarterly Balance Sheet")
    if balance_sheet:
        st.subheader("""**Quarterly balance sheet** for """ + selected_stock)
        display_balancesheet = (stock_data.quarterly_balance_sheet)
        if display_balancesheet.empty == True:
            st.write("No data available at the moment")
        else:
            st.write(display_balancesheet)
    
    #checkbox to display quarterly cashflow for searched ticker
    cashflow = st.sidebar.checkbox("Quarterly Cashflow")
    if cashflow:
        st.subheader("""**Quarterly cashflow** for """ + selected_stock)
        display_cashflow = (stock_data.quarterly_cashflow)
        if display_cashflow.empty == True:
            st.write("No data available at the moment")
        else:
            st.write(display_cashflow)
    
    #checkbox to display quarterly earnings for searched ticker
    earnings = st.sidebar.checkbox("Quarterly Earnings")
    if earnings:
        st.subheader("""**Quarterly earnings** for """ + selected_stock)
        display_earnings = (stock_data.quarterly_earnings)
        if display_earnings.empty == True:
            st.write("No data available at the moment")
        else:
            st.write(display_earnings)
    
    #checkbox to display list of analysts recommendation for searched ticker
    analyst_recommendation = st.sidebar.checkbox("Analysts Recommendation")
    if analyst_recommendation:
        st.subheader("""**Analysts recommendation** for """ + selected_stock)
        display_analyst_rec = (stock_data.recommendations)
        st.write(display_analyst_rec)

    sustainability = st.sidebar.checkbox("Sustainability")
    if sustainability:
        st.subheader("""**Data on Sustainabilility** for """ + selected_stock)
        display_sustainability = stock_data.sustainability
        st.write(display_sustainability)

# Run the main function
if __name__ == "__main__":
  main()

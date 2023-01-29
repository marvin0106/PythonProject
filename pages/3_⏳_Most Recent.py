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
#import streamlit.components.v1 as components
import mpld3
import locale
import datetime

st.set_page_config(
    page_title="InsidersInvest • Most Recent",
    page_icon="⏳",
    layout="wide")

#plt.style.use("default")
plt.style.use("seaborn-darkgrid")

print(plt.style.available)

st.sidebar.title("Stock Filter")
companies_input = st.sidebar.text_input("Enter a comma-separated list of company tickers:", "")
companies_input = companies_input.replace(" ", "")
companies = companies_input.split(",")

# Function for translating tickers into names: 

#def get_company_name(ticker):
#    company_info = yf.Ticker(ticker).info
#    name = company_info["longName"]
#    return name

#print(yf.Ticker("msft").info["longName"])
#print(get_company_name("msft"))

# =============================================================================
# Text Section
# =============================================================================

st.title("Recent Insider Trades")
#st.markdown("This table contains the most recent SEC-Filings for insider trading purchases & sales.")
st.markdown("This page reflects the most recent 1000 insider Trades sorted by SEC-Filing date. Also, you may apply filters to search for a specific company in the database. The tabs <Chart> and <Performance> then allow you to dive further in depth into insider trading data selected by you.")



with st.sidebar: 
    st.sidebar.title("Stock Search")
    Stocklist = pd.read_excel("Stocklist.xlsx")
    StocksnTickers = Stocklist.iloc[1:, [0,1]]
    StocksnTickers.columns = ['Ticker', 'Company Name']
    
    search_term = st.sidebar.text_input("Ticker or Company Name Search")
    
    filtered_df = StocksnTickers[(StocksnTickers['Company Name'].str.contains(search_term, case=False, na=False)) | (StocksnTickers['Ticker'].str.contains(search_term, case=False, na=False))]
    st.dataframe(filtered_df)

# =============================================================================

# Filter Box: 
if companies_input:
    st.success(" Stock Filter for: " + companies_input.upper(), icon = "✅")
#    st.markdown(get_company_name(companies_input))
else:
    st.warning(" Enter a comma-separated list of company tickers to filter", icon ="💡")
    
tab1, tab2, tab3 = st.tabs(["Table", "Chart", "Performance"])

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
        with tab2: 
            st.markdown("")  
            try:
                def get_stock_data(ticker, period):
                    stock_data = yf.Ticker(ticker).history(period=period)
                    return stock_data
            except NameError:
                st.warning(" Stock filter not applied, therefore no chart can be displayed here.", icon ="❌")
                    
    # Stock Chart
  
            ticker_symbol = company
            
            # Get the selected interval
            interval = 4
            
            # Get the current date
            now = pd.to_datetime('now')
            
            # Calculate the start date of the interval
            four_months_ago = now - pd.DateOffset(months=interval)

            insider.iloc[:, 1] = pd.to_datetime(insider.iloc[:, 1], format="%Y-%m-%d")
            # Filter the insider dataframe to only include rows where the date is within the selected interval
            filtered_insider = insider[(insider.iloc[:,1] >= four_months_ago) & (insider.iloc[:,1] <= now)]

        
            # Use the filtered dataframe to define the x_values
            x_values = filtered_insider.iloc[:,1]
            
            
            periodx = f"{interval}y"

            if ticker_symbol:
              st.header(str.upper(ticker_symbol) + " - Stock Data - 4y")
              stock_data = get_stock_data(ticker_symbol, periodx)
              if "Date" in stock_data.columns:
                stock_data.reset_index(inplace=True)    
                stock_data.set_index("Date", inplace=True, date_format="YYYY-MM-DD")
            try: 
                st.line_chart(stock_data['Close'])
            except NameError:
                st.warning(" Stock filter not applied, therefore no chart can be displayed here.", icon ="❌")
            
            
            
            insider.iloc[:,1] = pd.to_datetime(insider.iloc[:,1])
            purchase_df = insider[insider.iloc[:,5].str.contains("Purchase")]
            purchase_df.to_csv("chosen_purchases.csv")
            sale_df = insider[insider.iloc[:,5].str.contains("Sale")]
            
            #now = pd.to_datetime("now")
            #four_months_ago = now - pd.DateOffset(days=start_date)
            
            #purchase_df = purchase_df[(purchase_df.iloc[:,1] > four_months_ago) & (purchase_df.iloc[:,1] <= now)]
            
            
            
            print(purchase_df)
            st.header("Table with Insider-Purchases")
            with st.expander("Click to Expand"):
                st.table(purchase_df)
            
            print(sale_df)
            st.header("Table with Insider-Sales:")
            with st.expander("Click to Expand"):
                st.table(sale_df)
            
            insider.iloc[:,1] = pd.to_datetime(insider.iloc[:,1])
            
            # Plot the "Close" price over time
            fig = plt.figure(figsize = (9,5), dpi=200)
            try:
                plt.plot(stock_data["Close"], color="k", linewidth = "1")
            except NameError: 
                st.warning(" Stock filter not applied, therefore no chart can be displayed here.", icon ="❌")
            plt.xlabel("Date")
            plt.ylabel("Price in $")
            plt.title(f"{ticker_symbol} ".upper()+ "Price", fontsize=16)
            plt.xticks(rotation=40, fontsize = 12, alpha=0.7)
            
            # Beauty Program for Plots: 
            plt.gca().spines["top"].set_alpha(0.0)    
            plt.gca().spines["bottom"].set_alpha(0.3)
            plt.gca().spines["right"].set_alpha(0.0)    
            plt.gca().spines["left"].set_alpha(0.3)   
            
            fig_html = mpld3.fig_to_html(fig)
            # For added Interactivity remove "#"
            #components.html(fig_html, height = 600)
            

            for index, row in purchase_df.iterrows():
                date = pd.to_datetime(row[1])
                plt.axvline(x=date, color="b", linestyle="dotted", linewidth=".85")
            
            for index, row in sale_df.iterrows():
                date = pd.to_datetime(row[1])
                plt.axvline(x=date, color="r", linestyle="dotted", linewidth=".85")
                
            # =======MATPLOTLIB INTEGRATED LEGEND
            plt.legend(frameon=False, fontsize =15, facecolor ="white")
            import matplotlib.patches as mpatches
            blue_patch = mpatches.Patch(color='blue', label='purchases')
            red_patch = mpatches.Patch(color='red', label='sales')
            plt.legend(handles=[blue_patch, red_patch],loc='upper left')
            # ========MATPLOTLIB INTEGRATED LEGEND END
            
            st.pyplot(fig)
            plt.show()
            
 
            
        
        with tab3:
            purchase_df = purchase_df.drop(columns=["Filing\xa0Date", "Owned", "ΔOwn"])
            purchase_df["Trade\xa0Date"] = purchase_df["Trade\xa0Date"].dt.date
            purchase_df.rename(columns={'Trade\xa0Date': 'Date'}, inplace=True)

            #st.table(purchase_df)
            
            #New separate DF to save Data on tickers through yfinance API
            new_df = pd.DataFrame(columns=['Date', 'Ticker', 'Closing Price'])
            
            locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' )
            
            for index, row in purchase_df.iterrows():
                ticker = row['Ticker']
                date = row['Date']
                old_price = row["Price"]
                date = date.strftime("%Y-%m-%d")
                
                # Download data
                stock_data = yf.download(ticker, start="2010-01-01", end=date, interval = "1d",threads=False)
                stock_data = stock_data.tail(1)
                stock_price = round(stock_data.loc[:, "Adj Close"].values[0], 2)
                purchase_df.loc[index, "Price"] = "{:.2f}".format(stock_price)

                
                
                # Get today's date - Automatically takes yesterdays closing 
                today = datetime.date.today()
                
                # Download data
                stock_data = yf.download(ticker, start="2010-01-01", end=today, interval = "1d")
                stock_data = stock_data.tail(1)

                stock_data.reset_index(inplace=True)    
                closing_price=stock_data["Adj Close"]
                closing_price = stock_data.iat[0,2]
                closing_price = locale.currency( closing_price, grouping = True )
                
                
                new_df = new_df.append({'Date': date, 'Ticker': ticker, 'Closing Price': closing_price}, ignore_index=True)
            
            
            purchase_df["Ticker"] = purchase_df["Ticker"].astype(str)
            purchase_df["Date"] = pd.to_datetime(purchase_df["Date"], format='%Y-%m-%d')
            new_df["Ticker"] = new_df["Ticker"].astype(str)
            new_df["Date"] = pd.to_datetime(new_df["Date"], format='%Y-%m-%d')
            
            # Cleaned up Dates to look better in Dataframe: 
            purchase_df["Date"] = purchase_df["Date"].dt.strftime('%Y-%m-%d')
            new_df["Date"] = new_df["Date"].dt.strftime('%Y-%m-%d')
            
            # merge the two dataframes using outer join
            merged_df = pd.merge(purchase_df, new_df, on=["Ticker", "Date"], how='outer')
            
            
            merged_df.columns = merged_df.columns.str.replace(' ', '_')
            
            
            merged_df['Price'] = pd.to_numeric(merged_df['Price'].str.replace('$',''))
            merged_df['Closing_Price'] = pd.to_numeric(merged_df['Closing_Price'].str.replace('$',''))
            
            merged_df['Percent_Change'] = (merged_df['Closing_Price'] - merged_df['Price'])/merged_df['Price']*100

            # Section where we introduce alpha: ===============================
            sp500 = pd.read_csv("/Users/marvinsilvafortes/Desktop/7. Semester/Econ mit Python x/Project/pages/sp500_index.csv")
           
            df_split = sp500['Date;S&P500'].str.split(";", expand=True)
            df_split.columns = ['Date', 'S&P500']
            sp500 = pd.concat([sp500, df_split], axis=1)
            sp500.drop(columns=["Date;S&P500"], inplace=True)
            sp500['Date'] = pd.to_datetime(sp500['Date'], format='%d.%m.%Y').dt.strftime('%Y-%m-%d')
            
            # convert 'Date' column in sp500 to datetime format
            sp500['Date'] = pd.to_datetime(sp500['Date'])
            sp500['Date'] = pd.to_datetime(sp500['Date'], format='%Y-%m-%d')
            
            
            # change format of 'Date' column in merged_df to match the format in sp500
            merged_df['Date'] = pd.to_datetime(merged_df['Date'])
            #merged_df['Date'] = merged_df['Date'].dt.strftime('%Y-%m-%d')
            merged_df['Date'] = pd.to_datetime(merged_df['Date'], format='%Y-%m-%d')

            merged_df = pd.merge(merged_df, sp500, on='Date')

            # ==End SNP500 value formatting and integrating
            merged_df['S&P500'] = pd.to_numeric(merged_df['S&P500'], errors='coerce')

            # Get the S&P500 value for the newest available date in the sp500 dataframe
            latest_sp500_value = sp500.loc[sp500['Date'] == sp500['Date'].max(), 'S&P500'].values[0]
            latest_sp500_value = pd.to_numeric(latest_sp500_value, errors='coerce')

            
            # Create a new column in the merged_df dataframe that calculates the percentage change
            merged_df['S&P500_PCT_Change'] = ( latest_sp500_value - merged_df['S&P500']) / merged_df['S&P500'] * 100
            merged_df["Alpha"] = merged_df["Percent_Change"] - merged_df["S&P500_PCT_Change"]
 
            

            print(merged_df)
            
            # END OF ALPHA ====================================================

            # Transform back before putting into Table:
            merged_df['Date'] = pd.to_datetime(merged_df['Date'], format='%Y-%m-%d').dt.strftime('%Y-%m-%d')
            merged_df['Price'] = merged_df['Price'].astype(str)
            merged_df['Closing_Price'] = merged_df['Closing_Price'].astype(str)
            merged_df['Price'] = "$"+merged_df['Price']
            merged_df['Closing_Price'] = "$"+merged_df['Closing_Price']
            merged_df = merged_df.rename(columns={'Closing_Price': 'Closing_Price_Today'})

            merged_df['Percent_Change'] = merged_df['Percent_Change'].round(2)
            merged_df['Percent_Change'] = merged_df['Percent_Change'].apply('{:.2f}%'.format)
            
            merged_df = merged_df.drop(columns=["Value"])

            
            # Take or Drop SnP500 at Trade Date 
            #merged_df = merged_df.drop("S&P500", axis=1)
            merged_df['S&P500'] = merged_df['S&P500'].round(2)
            
            merged_df['S&P500_PCT_Change'] = merged_df['S&P500_PCT_Change'].round(2)
            merged_df['S&P500_PCT_Change'] = merged_df['S&P500_PCT_Change'].apply('{:.2f}%'.format)
            
            merged_df['Alpha'] = merged_df['Alpha'].round(2)
            merged_df['Alpha'] = merged_df['Alpha'].apply('{:.2f}%'.format)
            merged_df.columns = merged_df.columns.str.replace('_', ' ')
            
            st.header("Purchase Performance per Trade")
            st.table(merged_df)
                   
            # st.header("Average Insider Trade Performance until today vs. Market Performance until today Bar-Chart")

            # st.write(type(merged_df['Percent_Change'][0]))
            # st.table(merged_df['Percent_Change"])
            # merged_df['Percent_Change'] = pd.to_numeric(merged_df['Percent_Change'].str.replace('%',''))
            # merged_df['S&P500_PCT_Change'] = pd.to_numeric(merged_df['S&P500_PCT_Change'].str.replace('%',''))
            # print(merged_df.columns)
            # st.write(merged_df.columns)
            
            
            
    except KeyError:
        st.warning(" Entered Ticker Filter <" + company.upper() +"> is Invalid or does not exist", icon ="⚠️")

insider.to_csv("chosen_companies.csv")


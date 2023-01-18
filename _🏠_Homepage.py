#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  2 17:20:37 2023

@author: marvinsilvafortes
"""

import streamlit as st
import pandas as pd

st.set_page_config(
    page_title ="Insidertrading Screener - Home",
    page_icon="📈",   
)

def main():
  st.title("Home")

  st.markdown("Welcome to the Insider Trading and Stock Analysis app! Here you can explore the latest insider trading activity and analyze stock data to make informed investment decisions.")

  st.image("/Users/marvinsilvafortes/Desktop/7. Semester/Econ mit Python x/Project/pages/homepage_image.jpg", width=600)

  st.sidebar.title("Andere Darstellungsmöglichkeiten")
  
  
if __name__ == "__main__":
  main()

st.header("General Info on Insider Trading")
st.markdown("etc.")
st.header("Project Members: ")
st.markdown("Possiblity for Pictures etc.")

st.header("Stock Names & Tickers")

Stocklist = pd.read_excel("Stocklist.xlsx")
#Stocklist = Stocklist.drop(index=0)
Stocklist = Stocklist.rename(index={0: 'new_title_1', 1: 'new_title_2'})
StocksnTickers = Stocklist.iloc[1:, [0,1]]

st.sidebar.header("Stock Ticker List")
st.sidebar.write(st.table(StocksnTickers))

expand_menu = st.sidebar.expander("Advanced options")

Stocklist = pd.read_excel("Stocklist.xlsx")
#Stocklist = Stocklist.drop(index=0)
Stocklist = Stocklist.rename(index={0: 'new_title_1', 1: 'new_title_2'})
StocksnTickers = Stocklist.iloc[1:, [0,1]]

st.table(StocksnTickers)


    
    
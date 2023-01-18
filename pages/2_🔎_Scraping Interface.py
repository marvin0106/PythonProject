#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 23 23:00:30 2022

@author: marvinsilvafortes
"""

import time
import pandas as pd
import streamlit as st

from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Create a main function
def main():
  # Create a page called "Favourite Stocks"
  st.sidebar.title("Stock Filter")
  st.sidebar.text("Enter a ticker symbol to select a stock:")
  ticker_symbol = st.sidebar.text_input("Ticker symbol")

st.title("Web Scraper")
st.markdown("This page allows you to scrape fresh data for later usage for the tab"+
        " - Insider trades -")
st.text("")
st.markdown("Furthermore it is possible to visualize found data in Dataframes displayed below")

if st.button("Start Scrape"):
        
    driver = webdriver.Chrome()
    driver.get("https://finviz.com/insidertrading.ashx")
    
    #Hide chrome 
    driver.set_window_position(-12000,0)
    
    time.sleep(10)
    
    # ==== TAKING CARE OF COOKIE NOTIFICATION ===== 
    #driver.find_element(By.XPATH, "//div[2]/div/button[3]").click()
    WebDriverWait(driver, 7).until(EC.element_to_be_clickable((By.XPATH,
                            "//div[2]/div/button[3]"))).click()
    
    # =============================================
    
    #Ausführende Personen
    owners = driver.find_elements(By.XPATH, "//table[2]/tbody/tr/td[2]/a")
    # =============================================================================
    ###Test ob die kacke funkt### Notiz: /a kann raus, damit column title dabei ist
    # for owner in owners:
    #     print(owner.text)
    # =============================================================================
    
    tickers = driver.find_elements(By.XPATH, "//table[2]/tbody/tr/td[1]/a")
    # =============================================================================
    # for aktie in tickers:
    #     print(aktie.text)
    # =============================================================================
    
    relationships = driver.find_elements(By.XPATH, "//table[2]/tbody/tr[position()>1]/td[3]")
    
    #Dates of trade:
    dates = driver.find_elements(By.XPATH, "//table[2]/tbody/tr[position()>1]/td[4]")
    
    #Buy, Sell or Option: 
    transactions = driver.find_elements(By.XPATH, "//table[2]/tbody/tr[position()>1]/td[5]")
    
    # ================= TRANSACTON VALUE ===================
    #At Cost per Share:
    costs = driver.find_elements(By.XPATH, "//table[2]/tbody/tr[position()>1]/td[6]")
    
    #Number of Shares Transaction: 
    shares = driver.find_elements(By.XPATH, "//table[2]/tbody/tr[position()>1]/td[7]")
    
    #Value of Transaction 
    valtransactions = driver.find_elements(By.XPATH, "//table[2]/tbody/tr[position()>1]/td[8]")
    # ================= END TRANSACTION VALUE ==============
    
    #Number of shares total: 
    numshares = driver.find_elements(By.XPATH, "//table[2]/tbody/tr[position()>1]/td[9]")
    
    #When was SEC Form filed? 
    SECs = driver.find_elements(By.XPATH, "//table[2]/tbody/tr[position()>1]/td[10]")
    
    
    #Neue Liste erstellen um Daten zu speichern, später dann in Excel import
    insiders=[]
    
    for i in range(len(shares)):
        temporary_dict={"Owner" : owners[i].text,
                        "Ticker" : tickers[i].text,
                        "Relationship" : relationships[i].text,
                        "Date" : dates[i].text,
                        "Transaction Type" : transactions[i].text,
                        "Cost per Share" : costs[i].text,
                        "Number of Shares" : shares[i].text,
                        "Value of Transaction in $" : valtransactions[i].text, 
                        "Total Number of Shares Outstanding" : numshares[i].text, 
                        "SEC filing date" : SECs[i].text}
        insiders.append(temporary_dict)
                        
    df = pd.DataFrame(insiders)
    
    df.to_excel("InsiderTradesScrape.xlsx", index=False)
    df.to_csv("InsiderTradesScrapeCSV.csv", index=False)
    
    time.sleep(2)
    driver.close()
    
    # =============================================================================
    # #-----------------------------------------------------------------
    # # First, import the openpyxl library
    # import openpyxl
    # 
    # # Next, open the Excel file and specify which sheet you want to modify
    # wb = openpyxl.load_workbook('InsiderTradesScrape.xlsx')
    # sheet = wb['Sheet1']
    # 
    # # Then, loop through the rows in the sheet and auto adjust the row width
    # for row in sheet.rows:
    #     sheet.row_dimensions[row].auto_size = True
    # 
    # # Finally, save the changes to the Excel file
    # wb.save('InsiderTradesScrape.xlsx')
    # #-----------------------------------------------------------------
    # =============================================================================
    
    for i in range(10):
        print("")
    print("Done with scraping Insider-Trading data!")
    for i in range(10):
        print("")
    
    import tkinter as tk
    from tkinter import messagebox
    
    import os
    
    def show_dialog(func, *args, **kwargs):
        # create root window, then hide it
        root = tk.Tk()
        root.withdraw()
    
        # create a mutable variable for storing the result
        result = []
    
        # local function to call the dialog after the
        # event loop starts
        def show_dialog():
    
            # show the dialog; this will block until the
            # dialog is dismissed by the user
            result.append(func(*args, **kwargs))
    
            # destroy the root window when the dialog is dismissed
            # note: this will cause the event loop (mainloop) to end
            root.destroy()
    
        # run the function after the event loop is initialized
        root.after_idle(show_dialog)
    
        # start the event loop, then kill the tcl interpreter
        # once the root window has been destroyed
        root.mainloop()
        root.quit()
    
        # pop the result and return
        return result.pop()
    
    result = show_dialog(messagebox.askokcancel, "Finished", 
                         "Scrape is finished, find at InsiderTradesScrape.xlsx")
    if result:
        print("you answered OK")
    else:
        print("you cancelled")
    
    os._exit(0)

insider_trading_data = pd.read_csv("/Users/marvinsilvafortes/Desktop/7. Semester/Econ mit Python x/Project/pages/InsiderTradesScrapeCSV.csv")

insider_trading_data["Date"] = pd.to_datetime(insider_trading_data["Date"], format="%b %d", infer_datetime_format=True, dayfirst=True)

#insider_trading_data["Date"] = insider_trading_data["Date"].str.replace("T00:00:00", "")

st.dataframe(insider_trading_data)


if __name__ == "__main__":
  main()



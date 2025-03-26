# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 18:22:42 2023

@author: marc-
"""
import streamlit as st

import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import textwrap

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

st.set_page_config(
    page_title="InsidersInvest • Case Studies",
    page_icon="🔎",
    layout="wide")

st.title("Case Studies")

image_path = "/workspaces/PythonProject/App/"

tab1 , tab2, tab3, tab4 = st.tabs(["Apple Inc.", "Microsoft", "Tesla", "Occidental"])

with tab1:
    Image = plt.imread(image_path + "Apple_logo_grey.png")
    st.image(Image, width=(150)	)
    st.header("Apple Inc.")
    
    st.markdown("Apple Inc. designs, manufactures, and markets smartphones, personal computers, tablets, wearables, and accessories worldwide. It also sells various related services. In addition, the company offers iPhone, a line of smartphones; Mac, a line of personal computers; iPad, a line of multi-purpose tablets; and wearables, home, and accessories comprising AirPods, Apple TV, Apple Watch, Beats products, and HomePod. Further, it provides AppleCare support and cloud services store services; and operates various platforms, including the App Store that allow customers to discover and download applications and digital content, such as books, music, video, games, and podcasts. Additionally, the company offers various services, such as Apple Arcade, a game subscription service; Apple Fitness+, a personalized fitness service; Apple Music, which offers users a curated listening experience with on-demand radio stations; Apple News+, a subscription news and magazine service; Apple TV+, which offers exclusive original content; Apple Card, a co-branded credit card; and Apple Pay, a cashless payment service, as well as licenses its intellectual property. The company serves consumers, and small and mid-sized businesses; and the education, enterprise, and government markets. It distributes third-party applications for its products through the App Store. The company also sells its products through its retail and online stores, and direct sales force; and third-party cellular network carriers, wholesalers, retailers, and resellers. Apple Inc. was incorporated in 1977 and is headquartered in Cupertino, California.")
    
    st.subheader("Headquarters")
    data = {'latitude': [37.334908], 'longitude': [-122.008629]}

    df = pd.DataFrame(data, columns=["latitude", "longitude"])

    st.map(df, zoom = 6)
    
    st.subheader("Current Share Prices")

    Stock_Tick="AAPL"

    stock_data = yf.Ticker(Stock_Tick).history(period="1y")

    # Make the datetime columns timezone unaware
    stock_data.index = stock_data.index.tz_localize(None)
    stock_data.index = stock_data.index.strftime('%Y-%m-%d')

    # Formattierte Daten von GPT integrieren; Evtl. hier Format ändern, da 
    #insidertradesscrapes.csv das format %b-%d hat -> %b steht hierbei für
    #englische abgekürzte notiertung: bsp: December > Dec

    dates = stock_data.index
    closing_prices = stock_data['Close']

    # wieder reformatieren, um angemessen zu plotten im nächsten Schritt
    dates = pd.to_datetime(dates)


    plt.plot(dates, closing_prices)
    plt.title(Stock_Tick + ' Stock Price')
    plt.ylabel('Closing Price ($ USD)')  
    plt.xlabel("Date")


    # Streamlit Plot: 
    st.line_chart(closing_prices)
    
    driver = webdriver.Chrome()
    driver.get("https://www.nasdaq.com/market-activity/stocks/aapl/insider-activity")
    
    driver.minimize_window()

    time.sleep(5)

    button = driver.find_element(by=By.ID, value="onetrust-accept-btn-handler")
    button.click()

    wait = WebDriverWait(driver, 10)

    table = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "insider-activity__data")))

    data = []

    rows = table.find_elements(By.TAG_NAME, "tr")
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        row_data = [cell.text for cell in cells]
        data.append(row_data)
        
    df = pd.DataFrame(data, columns=["Insider Trade", "3 Months", "12 Months"])

    df = df.drop(index=0)
    
    def remove_parenthesis(val):
        if val.startswith("("):
            return -int(val.replace("(","").replace(")","").replace(",",""))
        else:
            try:
                return int(val.replace(",",""))
            except ValueError:
                return int(val)

    df[['3 Months','12 Months']] = df[['3 Months','12 Months']].applymap(remove_parenthesis)

    st.subheader("Number of Insider Trades")
    
    x = df["Insider Trade"]
    bar1 = df["3 Months"]
    bar2 = df["12 Months"]

    fig, ax = plt.subplots()

    x_pos = np.arange(len(x))

    ax.bar(x_pos - 0.2, bar1, 0.4, label="3 Months", color="red")
    ax.bar(x_pos + 0.2, bar2, 0.4, label= "12 Months", color="grey")

    ax.set_xticks(x_pos)
    ax.set_xticklabels([textwrap.fill(text, 15) for text in x])

    ax.set_title('Number of Insider Trades')
    ax.legend(loc = "upper left")
    ax.set_yticklabels([])
    ax.set_yticks([])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(True)
    ax.spines['left'].set_visible(True)

    for i in ax.containers:
        ax.bar_label(i, label_type='edge')

    st.pyplot(fig)
    
    parent_class = driver.find_element(By.CLASS_NAME, "insider-activity__section.insider-activity__section--insider-shares")
    table = parent_class.find_element(By.CLASS_NAME, "insider-activity__data")

    data = []

    rows = table.find_elements(By.TAG_NAME, "tr")
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        row_data = [cell.text for cell in cells]
        data.append(row_data)
    
    df = pd.DataFrame(data, columns=["Insider Trade", "3 Months", "12 Months"])

    df = df.drop(index=0)
    
    def remove_parenthesis(val):
        if val.startswith("("):
            return -int(val.replace("(","").replace(")","").replace(",",""))
        else:
            try:
                return int(val.replace(",",""))
            except ValueError:
                return int(val)

    df[['3 Months','12 Months']] = df[['3 Months','12 Months']].applymap(remove_parenthesis)
    
    st.subheader("Number of Insider Shares Traded")
    
    x = df["Insider Trade"]
    bar1 = round(df["3 Months"] / 1000, 0)
    bar2 = round(df["12 Months"] / 1000, 0)

    fig, ax = plt.subplots()

    x_pos = np.arange(len(x))

    ax.bar(x_pos - 0.2, bar1, 0.4, label="3 Months", color="red")
    ax.bar(x_pos + 0.2, bar2, 0.4, label= "12 Months", color="grey")

    ax.set_xticks(x_pos)
    ax.set_xticklabels([textwrap.fill(text, 15) for text in x])

    ax.set_title('Number of Insider Shares Traded in Thousands')
    ax.legend(loc = "upper left")
    ax.set_yticklabels([])
    ax.set_yticks([])
    ax.axhline(y=0, color='black', linewidth=1)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(True)
    ax.spines['left'].set_visible(True)

    for i in ax.containers:
        ax.bar_label(i, label_type='edge')

    st.pyplot(fig)

    nsb12 = df.iloc[0,2]
    nss12 = df.iloc[1,2]
    tst12 = nsb12 + nss12

    chart = [nsb12, nss12]
    label = ["Shares Bought", "Shares Sold"]

    fig, ax = plt.subplots()
     
    ax.pie(chart, labels=label, autopct='%1.1f%%', colors=("grey", "red"))

    ax.set_title("Distribution of Buys and Sells")
    ax.legend(loc="lower left")
    st.pyplot(fig)
       
    parent_class = driver.find_element(By.CLASS_NAME, "insider-activity__section.insider-activity__section--scrollable.insider-activity__section--transactions")
    table = parent_class.find_element(By.CLASS_NAME, "insider-activity__data")

    data = []

    rows = table.find_elements(By.TAG_NAME, "tr")
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        row_data = [cell.text for cell in cells]
        data.append(row_data)
         
    df = pd.DataFrame(data, columns=["Insider", "Relation", "Last Date", "Transaction", "Owner Type", "Shares Traded", "Price", "Shares Held"])

    df = df.drop(index=0)

    st.subheader("Most Recent Insider Trades")

    st.dataframe(df)
    
    st.subheader("InsidersInvest's Insight")
    
    st.markdown("Looking at Apple's share price performance over the last year, declining by about 25%, we saw exclusively sales of insiders in the period. Additionally, the activity of insiders is not equally distributed over the last 12 months. Insiders activity was close to 0 in the last 3 months.")
    
with tab2:
    Image = plt.imread(image_path + "Microsoft_logo.png")
    st.image(Image, width=(200)	)
    st.header("Microsoft Corporation")
    
    st.markdown("Microsoft Corporation develops, licenses, and supports software, services, devices, and solutions worldwide. The company operates in three segments: Productivity and Business Processes, Intelligent Cloud, and More Personal Computing. The Productivity and Business Processes segment offers Office, Exchange, SharePoint, Microsoft Teams, Office 365 Security and Compliance, Microsoft Viva, and Skype for Business; Skype, Outlook.com, OneDrive, and LinkedIn; and Dynamics 365, a set of cloud-based and on-premises business solutions for organizations and enterprise divisions. The Intelligent Cloud segment licenses SQL, Windows Servers, Visual Studio, System Center, and related Client Access Licenses; GitHub that provides a collaboration platform and code hosting service for developers; Nuance provides healthcare and enterprise AI solutions; and Azure, a cloud platform. It also offers enterprise support, Microsoft consulting, and nuance professional services to assist customers in developing, deploying, and managing Microsoft server and desktop solutions; and training and certification on Microsoft products. The More Personal Computing segment provides Windows original equipment manufacturer (OEM) licensing and other non-volume licensing of the Windows operating system; Windows Commercial, such as volume licensing of the Windows operating system, Windows cloud services, and other Windows commercial offerings; patent licensing; and Windows Internet of Things. It also offers Surface, PC accessories, PCs, tablets, gaming and entertainment consoles, and other devices; Gaming, including Xbox hardware, and Xbox content and services; video games and third-party video game royalties; and Search, including Bing and Microsoft advertising. The company sells its products through OEMs, distributors, and resellers; and directly through digital marketplaces, online stores, and retail stores. Microsoft Corporation was founded in 1975 and is headquartered in Redmond, Washington.")

    st.subheader("Headquarters")
    data = {'latitude': [47.643605], 'longitude': [-122.130336]}

    df = pd.DataFrame(data, columns=["latitude", "longitude"])

    st.map(df, zoom = 6)
    
    st.subheader("Current Share Prices")

    Stock_Tick="Msft"

    stock_data = yf.Ticker(Stock_Tick).history(period="1y")

    # Make the datetime columns timezone unaware
    stock_data.index = stock_data.index.tz_localize(None)
    stock_data.index = stock_data.index.strftime('%Y-%m-%d')

    # Formattierte Daten von GPT integrieren; Evtl. hier Format ändern, da 
    #insidertradesscrapes.csv das format %b-%d hat -> %b steht hierbei für
    #englische abgekürzte notiertung: bsp: December > Dec

    dates = stock_data.index
    closing_prices = stock_data['Close']

    # wieder reformatieren, um angemessen zu plotten im nächsten Schritt
    dates = pd.to_datetime(dates)


    plt.plot(dates, closing_prices)
    plt.title(Stock_Tick + ' Stock Price')
    plt.ylabel('Closing Price ($ USD)')  
    plt.xlabel("Date")


    # Streamlit Plot: 
    st.line_chart(closing_prices)

    driver = webdriver.Chrome()
    driver.get("https://www.nasdaq.com/market-activity/stocks/msft/insider-activity")

    driver.minimize_window()

    time.sleep(5)

    button = driver.find_element(by=By.ID, value="onetrust-accept-btn-handler")
    button.click()

    wait = WebDriverWait(driver, 10)

    table = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "insider-activity__data")))

    data = []

    rows = table.find_elements(By.TAG_NAME, "tr")
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        row_data = [cell.text for cell in cells]
        data.append(row_data)
        
    df = pd.DataFrame(data, columns=["Insider Trade", "3 Months", "12 Months"])

    df = df.drop(index=0)

    def remove_parenthesis(val):
        if val.startswith("("):
            return -int(val.replace("(","").replace(")","").replace(",",""))
        else:
            try:
                return int(val.replace(",",""))
            except ValueError:
                return int(val)

    df[['3 Months','12 Months']] = df[['3 Months','12 Months']].applymap(remove_parenthesis)

    st.subheader("Number of Insider Trades")

    x = df["Insider Trade"]
    bar1 = df["3 Months"]
    bar2 = df["12 Months"]

    fig, ax = plt.subplots()

    x_pos = np.arange(len(x))

    ax.bar(x_pos - 0.2, bar1, 0.4, label="3 Months", color="red")
    ax.bar(x_pos + 0.2, bar2, 0.4, label= "12 Months", color="grey")

    ax.set_xticks(x_pos)
    ax.set_xticklabels([textwrap.fill(text, 15) for text in x])

    ax.set_title('Number of Insider Trades')
    ax.legend(loc = "upper left")
    ax.set_yticklabels([])
    ax.set_yticks([])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(True)
    ax.spines['left'].set_visible(True)

    for i in ax.containers:
        ax.bar_label(i, label_type='edge')

    st.pyplot(fig)

    parent_class = driver.find_element(By.CLASS_NAME, "insider-activity__section.insider-activity__section--insider-shares")
    table = parent_class.find_element(By.CLASS_NAME, "insider-activity__data")

    data = []

    rows = table.find_elements(By.TAG_NAME, "tr")
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        row_data = [cell.text for cell in cells]
        data.append(row_data)

    df = pd.DataFrame(data, columns=["Insider Trade", "3 Months", "12 Months"])

    df = df.drop(index=0)

    def remove_parenthesis(val):
        if val.startswith("("):
            return -int(val.replace("(","").replace(")","").replace(",",""))
        else:
            try:
                return int(val.replace(",",""))
            except ValueError:
                return int(val)

    df[['3 Months','12 Months']] = df[['3 Months','12 Months']].applymap(remove_parenthesis)

    st.subheader("Number of Insider Shares Traded")

    x = df["Insider Trade"]
    bar1 = round(df["3 Months"] / 1000, 0)
    bar2 = round(df["12 Months"] / 1000, 0)

    fig, ax = plt.subplots()

    x_pos = np.arange(len(x))

    ax.bar(x_pos - 0.2, bar1, 0.4, label="3 Months", color="red")
    ax.bar(x_pos + 0.2, bar2, 0.4, label= "12 Months", color="grey")

    ax.set_xticks(x_pos)
    ax.set_xticklabels([textwrap.fill(text, 15) for text in x])

    ax.set_title('Number of Insider Shares Traded in Thousands')
    ax.legend(loc = "upper left")
    ax.set_yticklabels([])
    ax.set_yticks([])
    ax.axhline(y=0, color='black', linewidth=1)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(True)
    ax.spines['left'].set_visible(True)

    for i in ax.containers:
        ax.bar_label(i, label_type='edge')

    st.pyplot(fig)
    
    nsb12 = df.iloc[0,2]
    nss12 = df.iloc[1,2]
    tst12 = nsb12 + nss12

    chart = [nsb12, nss12]
    label = ["Shares Bought", "Shares Sold"]

    fig, ax = plt.subplots()
     
    ax.pie(chart, labels=label, autopct='%1.1f%%', colors=("grey", "red"))

    ax.set_title("Distribution of Buys and Sells")
    ax.legend(loc="lower left")
    st.pyplot(fig)
    
    parent_class = driver.find_element(By.CLASS_NAME, "insider-activity__section.insider-activity__section--scrollable.insider-activity__section--transactions")
    table = parent_class.find_element(By.CLASS_NAME, "insider-activity__data")

    data = []

    rows = table.find_elements(By.TAG_NAME, "tr")
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        row_data = [cell.text for cell in cells]
        data.append(row_data)
         
    df = pd.DataFrame(data, columns=["Insider", "Relation", "Last Date", "Transaction", "Owner Type", "Shares Traded", "Price", "Shares Held"])

    df = df.drop(index=0)

    st.subheader("Most Recent Insider Trades")

    st.dataframe(df)
    
    st.subheader("InsidersInvest's Insight")
    
    st.markdown("Microsoft's Insiders bought and sold almost an equal amount of shares over the last 12 months, with less activity over the last 3 months compared with the previous 9 months. This sets Microsoft apart from our other case studies due to the equal distribution of buys and sells.")
    

with tab3:
    Image = plt.imread(image_path + "Tesla_Motors.png")
    st.image(Image, width=(125)	)
    st.header("Tesla, Inc.")
    
    st.markdown("Tesla, Inc. designs, develops, manufactures, leases, and sells electric vehicles, and energy generation and storage systems in the United States, China, and internationally. The company operates in two segments, Automotive, and Energy Generation and Storage. The Automotive segment offers electric vehicles, as well as sells automotive regulatory credits. It provides sedans and sport utility vehicles through direct and used vehicle sales, a network of Tesla Superchargers, and in-app upgrades; and purchase financing and leasing services. This segment is also involved in the provision of non-warranty after-sales vehicle services, sale of used vehicles, retail merchandise, and vehicle insurance, as well as sale of products to third party customers; services for electric vehicles through its company-owned service locations, and Tesla mobile service technicians; and vehicle limited warranties and extended service plans. The Energy Generation and Storage segment engages in the design, manufacture, installation, sale, and leasing of solar energy generation and energy storage products, and related services to residential, commercial, and industrial customers and utilities through its website, stores, and galleries, as well as through a network of channel partners. This segment also offers service and repairs to its energy product customers, including under warranty; and various financing options to its solar customers. The company was formerly known as Tesla Motors, Inc. and changed its name to Tesla, Inc. in February 2017. Tesla, Inc. was incorporated in 2003 and is headquartered in Austin, Texas.")
    
    st.subheader("Headquarters")
    data = {'latitude': [37.393974], 'longitude': [-122.149355]} 

    df = pd.DataFrame(data, columns=["latitude", "longitude"])

    st.map(df, zoom = 6)
    
    st.subheader("Current Share Prices")

    Stock_Tick="TSLA"

    stock_data = yf.Ticker(Stock_Tick).history(period="1y")

    # Make the datetime columns timezone unaware
    stock_data.index = stock_data.index.tz_localize(None)
    stock_data.index = stock_data.index.strftime('%Y-%m-%d')

    # Formattierte Daten von GPT integrieren; Evtl. hier Format ändern, da 
    #insidertradesscrapes.csv das format %b-%d hat -> %b steht hierbei für
    #englische abgekürzte notiertung: bsp: December > Dec

    dates = stock_data.index
    closing_prices = stock_data['Close']

    # wieder reformatieren, um angemessen zu plotten im nächsten Schritt
    dates = pd.to_datetime(dates)


    plt.plot(dates, closing_prices)
    plt.title(Stock_Tick + ' Stock Price')
    plt.ylabel('Closing Price ($ USD)')  
    plt.xlabel("Date")


    # Streamlit Plot: 
    st.line_chart(closing_prices)

    driver = webdriver.Chrome()
    driver.get("https://www.nasdaq.com/market-activity/stocks/tsla/insider-activity")

    driver.minimize_window()

    time.sleep(5)

    button = driver.find_element(by=By.ID, value="onetrust-accept-btn-handler")
    button.click()

    wait = WebDriverWait(driver, 10)

    table = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "insider-activity__data")))

    data = []

    rows = table.find_elements(By.TAG_NAME, "tr")
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        row_data = [cell.text for cell in cells]
        data.append(row_data)
        
    df = pd.DataFrame(data, columns=["Insider Trade", "3 Months", "12 Months"])

    df = df.drop(index=0)

    def remove_parenthesis(val):
        if val.startswith("("):
            return -int(val.replace("(","").replace(")","").replace(",",""))
        else:
            try:
                return int(val.replace(",",""))
            except ValueError:
                return int(val)

    df[['3 Months','12 Months']] = df[['3 Months','12 Months']].applymap(remove_parenthesis)

    st.subheader("Number of Insider Trades")

    x = df["Insider Trade"]
    bar1 = df["3 Months"]
    bar2 = df["12 Months"]

    fig, ax = plt.subplots()

    x_pos = np.arange(len(x))

    ax.bar(x_pos - 0.2, bar1, 0.4, label="3 Months", color="red")
    ax.bar(x_pos + 0.2, bar2, 0.4, label= "12 Months", color="grey")

    ax.set_xticks(x_pos)
    ax.set_xticklabels([textwrap.fill(text, 15) for text in x])

    ax.set_title('Number of Insider Trades')
    ax.legend(loc = "upper left")
    ax.set_yticklabels([])
    ax.set_yticks([])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(True)
    ax.spines['left'].set_visible(True)

    for i in ax.containers:
        ax.bar_label(i, label_type='edge')

    st.pyplot(fig)

    parent_class = driver.find_element(By.CLASS_NAME, "insider-activity__section.insider-activity__section--insider-shares")
    table = parent_class.find_element(By.CLASS_NAME, "insider-activity__data")

    data = []

    rows = table.find_elements(By.TAG_NAME, "tr")
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        row_data = [cell.text for cell in cells]
        data.append(row_data)

    df = pd.DataFrame(data, columns=["Insider Trade", "3 Months", "12 Months"])

    df = df.drop(index=0)

    def remove_parenthesis(val):
        if val.startswith("("):
            return -int(val.replace("(","").replace(")","").replace(",",""))
        else:
            try:
                return int(val.replace(",",""))
            except ValueError:
                return int(val)

    df[['3 Months','12 Months']] = df[['3 Months','12 Months']].applymap(remove_parenthesis)

    st.subheader("Number of Insider Shares Traded")

    x = df["Insider Trade"]
    bar1 = round(df["3 Months"] / 1000, 0)
    bar2 = round(df["12 Months"] / 1000, 0)

    fig, ax = plt.subplots()

    x_pos = np.arange(len(x))

    ax.bar(x_pos - 0.2, bar1, 0.4, label="3 Months", color="red")
    ax.bar(x_pos + 0.2, bar2, 0.4, label= "12 Months", color="grey")

    ax.set_xticks(x_pos)
    ax.set_xticklabels([textwrap.fill(text, 15) for text in x])

    ax.set_title('Number of Insider Shares Traded in Thousands')
    ax.legend(loc = "upper left")
    ax.set_yticklabels([])
    ax.set_yticks([])
    ax.axhline(y=0, color='black', linewidth=1)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(True)
    ax.spines['left'].set_visible(True)

    for i in ax.containers:
        ax.bar_label(i, label_type='edge')

    st.pyplot(fig)
    
    nsb12 = df.iloc[0,2]
    nss12 = df.iloc[1,2]
    tst12 = nsb12 + nss12

    chart = [nsb12, nss12]
    label = ["Shares Bought", "Shares Sold"]

    fig, ax = plt.subplots()
     
    ax.pie(chart, labels=label, autopct='%1.1f%%', colors=("grey", "red"))

    ax.set_title("Distribution of Buys and Sells")
    ax.legend(loc="lower left")
    st.pyplot(fig)
    
    parent_class = driver.find_element(By.CLASS_NAME, "insider-activity__section.insider-activity__section--scrollable.insider-activity__section--transactions")
    table = parent_class.find_element(By.CLASS_NAME, "insider-activity__data")

    data = []

    rows = table.find_elements(By.TAG_NAME, "tr")
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        row_data = [cell.text for cell in cells]
        data.append(row_data)
         
    df = pd.DataFrame(data, columns=["Insider", "Relation", "Last Date", "Transaction", "Owner Type", "Shares Traded", "Price", "Shares Held"])

    df = df.drop(index=0)

    st.subheader("Most Recent Insider Trades")

    st.dataframe(df)
    
    st.subheader("InsidersInvest's Insight")
    
    st.markdown("Over the last 12 months, Tesla Insiders sold current holdings and did not increase their positions. Famously, the CEO of Tesla, Elon Musk, was heavily involved in a project outside of Tesla, the acquisition of the social media platform Twitter. On the one hand, Elon had to sell Tesla shares to finance the transaction and, on the other hand, other insiders might have sold parts of their positions aswell due to the process.")

with tab4:
    Image = plt.imread(image_path + "Occidental-Petroleum.png")
    st.image(Image, width=(150)	)
    st.header("Occidental Petroleum Corporation")
    
    st.markdown("Occidental Petroleum Corporation, together with its subsidiaries, engages in the acquisition, exploration, and development of oil and gas properties in the United States, the Middle East, Africa, and Latin America. It operates through three segments: Oil and Gas, Chemical, and Midstream and Marketing. The company’s Oil and Gas segment explores for, develops, and produces oil and condensate, natural gas liquids (NGLs), and natural gas. Its Chemical segment manufactures and markets basic chemicals, including chlorine, caustic soda, chlorinated organics, potassium chemicals, ethylene dichloride, chlorinated isocyanurates, sodium silicates, and calcium chloride; vinyls comprising vinyl chloride monomer, polyvinyl chloride, and ethylene. The Midstream and Marketing segment gathers, processes, transports, stores, purchases, and markets oil, condensate, NGLs, natural gas, carbon dioxide, and power. This segment also trades around its assets consisting of transportation and storage capacity; and invests in entities. Occidental Petroleum Corporation was founded in 1920 and is headquartered in Houston, Texas.")
    
    st.subheader("Headquarters")
    data = {'latitude': [29.730421], 'longitude': [-95.432155]}

    df = pd.DataFrame(data, columns=["latitude", "longitude"])

    st.map(df, zoom = 6)
    
    st.subheader("Current Share Prices")

    Stock_Tick="OXY"

    stock_data = yf.Ticker(Stock_Tick).history(period="1y")

    # Make the datetime columns timezone unaware
    stock_data.index = stock_data.index.tz_localize(None)
    stock_data.index = stock_data.index.strftime('%Y-%m-%d')

    # Formattierte Daten von GPT integrieren; Evtl. hier Format ändern, da 
    #insidertradesscrapes.csv das format %b-%d hat -> %b steht hierbei für
    #englische abgekürzte notiertung: bsp: December > Dec

    dates = stock_data.index
    closing_prices = stock_data['Close']

    # wieder reformatieren, um angemessen zu plotten im nächsten Schritt
    dates = pd.to_datetime(dates)


    plt.plot(dates, closing_prices)
    plt.title(Stock_Tick + ' Stock Price')
    plt.ylabel('Closing Price ($ USD)')  
    plt.xlabel("Date")


    # Streamlit Plot: 
    st.line_chart(closing_prices)

    driver = webdriver.Chrome()
    driver.get("https://www.nasdaq.com/market-activity/stocks/oxy/insider-activity")

    driver.minimize_window()

    time.sleep(5)

    button = driver.find_element(by=By.ID, value="onetrust-accept-btn-handler")
    button.click()

    wait = WebDriverWait(driver, 10)

    table = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "insider-activity__data")))

    data = []

    rows = table.find_elements(By.TAG_NAME, "tr")
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        row_data = [cell.text for cell in cells]
        data.append(row_data)
        
    df = pd.DataFrame(data, columns=["Insider Trade", "3 Months", "12 Months"])

    df = df.drop(index=0)

    def remove_parenthesis(val):
        if val.startswith("("):
            return -int(val.replace("(","").replace(")","").replace(",",""))
        else:
            try:
                return int(val.replace(",",""))
            except ValueError:
                return int(val)

    df[['3 Months','12 Months']] = df[['3 Months','12 Months']].applymap(remove_parenthesis)

    st.subheader("Number of Insider Trades")

    x = df["Insider Trade"]
    bar1 = df["3 Months"]
    bar2 = df["12 Months"]

    fig, ax = plt.subplots()

    x_pos = np.arange(len(x))

    ax.bar(x_pos - 0.2, bar1, 0.4, label="3 Months", color="red")
    ax.bar(x_pos + 0.2, bar2, 0.4, label= "12 Months", color="grey")

    ax.set_xticks(x_pos)
    ax.set_xticklabels([textwrap.fill(text, 15) for text in x])

    ax.set_title('Number of Insider Trades')
    ax.legend(loc = "upper left")
    ax.set_yticklabels([])
    ax.set_yticks([])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(True)
    ax.spines['left'].set_visible(True)

    for i in ax.containers:
        ax.bar_label(i, label_type='edge')

    st.pyplot(fig)

    parent_class = driver.find_element(By.CLASS_NAME, "insider-activity__section.insider-activity__section--insider-shares")
    table = parent_class.find_element(By.CLASS_NAME, "insider-activity__data")

    data = []

    rows = table.find_elements(By.TAG_NAME, "tr")
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        row_data = [cell.text for cell in cells]
        data.append(row_data)

    df = pd.DataFrame(data, columns=["Insider Trade", "3 Months", "12 Months"])

    df = df.drop(index=0)

    def remove_parenthesis(val):
        if val.startswith("("):
            return -int(val.replace("(","").replace(")","").replace(",",""))
        else:
            try:
                return int(val.replace(",",""))
            except ValueError:
                return int(val)

    df[['3 Months','12 Months']] = df[['3 Months','12 Months']].applymap(remove_parenthesis)

    st.subheader("Number of Insider Shares Traded")

    x = df["Insider Trade"]
    bar1 = round(df["3 Months"] / 1000, 0)
    bar2 = round(df["12 Months"] / 1000, 0)

    fig, ax = plt.subplots()

    x_pos = np.arange(len(x))

    ax.bar(x_pos - 0.2, bar1, 0.4, label="3 Months", color="red")
    ax.bar(x_pos + 0.2, bar2, 0.4, label= "12 Months", color="grey")

    ax.set_xticks(x_pos)
    ax.set_xticklabels([textwrap.fill(text, 15) for text in x])

    ax.set_title('Number of Insider Shares Traded in Thousands')
    ax.legend(loc="upper left")
    ax.set_yticklabels([])
    ax.set_yticks([])
    ax.axhline(y=0, color='black', linewidth=1)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(True)
    ax.spines['left'].set_visible(True)

    for i in ax.containers:
        ax.bar_label(i, label_type='edge')

    st.pyplot(fig)
    
    nsb12 = df.iloc[0,2]
    nss12 = df.iloc[1,2]
    tst12 = nsb12 + nss12

    chart = [nsb12, nss12]
    label = ["Shares Bought", "Shares Sold"]

    fig, ax = plt.subplots()
     
    ax.pie(chart, labels=label, autopct='%1.1f%%', colors=("grey", "red"))

    ax.set_title("Distribution of Buys and Sells")
    ax.legend(loc="lower left")
    st.pyplot(fig)

    parent_class = driver.find_element(By.CLASS_NAME, "insider-activity__section.insider-activity__section--scrollable.insider-activity__section--transactions")
    table = parent_class.find_element(By.CLASS_NAME, "insider-activity__data")

    data = []

    rows = table.find_elements(By.TAG_NAME, "tr")
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        row_data = [cell.text for cell in cells]
        data.append(row_data)
         
    df = pd.DataFrame(data, columns=["Insider", "Relation", "Last Date", "Transaction", "Owner Type", "Shares Traded", "Price", "Shares Held"])

    df = df.drop(index=0)

    st.subheader("Most Recent Insider Trades")

    st.dataframe(df)
    
    st.subheader("InsidersInvest's Insight")
    
    st.markdown("In contrast to the other cases that we discussed, Occidental Petroleum Insider's mainly bought additional shares, one of them being the investment firm Berkshire Hathaway, lead by Warren Buffet. Again, this case shows again the positive relation between insider activity and share price development, since the share price of OXY incresed from USD37.7 to USD67.1. ")



    


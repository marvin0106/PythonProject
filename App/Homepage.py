# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 22:32:49 2023

@author: Alexander-NB
"""

with open('style.css', 'w') as file:
    file.write("body {background-image: url('background.png'); background-size: cover;}")

import streamlit as st
import pandas as pd


st.set_page_config(page_title="InsidersInvest", page_icon="📈",
                  layout='wide', initial_sidebar_state='expanded')
import base64
def add_bg_from_local(image_file):
    with open(r"C:\Users\Alexander-NB\OneDrive\Desktop\Uni\6. Semester\FEWP\Project\App\{}".format(image_file), "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )
add_bg_from_local('background.png')

   
def main():
    # Add background
    
    # Add a logo or banner
    col1, col2, col3 = st.columns(3)

    with col1:
        st.write(' ')

    with col2:
        st.image("logo_new.png")

    with col3:
    # Add button
        Newsletter_button = st.button("Sign up for the newsletter")
        if Newsletter_button:
          st.write("Send e-Mail to: Insiders@Invest.io")  
        else:
            st.write("")

#####
    st.markdown("<p style='text-align: center; font-size: 50px; font-weight: 1000;'>Welcome to InsidersInvest!</p>", unsafe_allow_html=True) 
    original_title1 = '<p style="text-align: center; font-weight: 700; font-size: 32px;">Your source for information about Insider Trading</p>'
    st.markdown(original_title1, unsafe_allow_html=True)
    
    original_title2 = '<p style="text-align: center; font-size: 25px; font-weight: 500">We bring Transparency into the market and help you to invest alongside the most successful managers in history!</p>'
    st.markdown(original_title2, unsafe_allow_html=True)
    
    
    # st.header('This is a header')
    # st.header('A header with _italics_ :blue[colors] and emojis :sunglasses:')
    # Use a consistent color scheme and typography
    
    col1, col2, col3 = st.columns(3)

    with col1:
        st.write(' ')

    with col2:
        st.image("CEOs.png")

    with col3:
        st.write(' ')
        
        
    # Add a section for features    
    st.markdown("<p style='font-size: 30px; font-weight: 625'>Features offered:</p>", unsafe_allow_html=True)
    st.markdown("<p style=' font-size: 25px; font-weight: 500;'>- Newsletter with information on insider activities of the largest US companies 	✅</p>", unsafe_allow_html=True)
    st.markdown("<p style=' font-size: 25px; font-weight: 500;'>- Monitor insider trading activity for all S&P500 companies 	✅</p>", unsafe_allow_html=True)
    st.markdown("<p style=' font-size: 25px; font-weight: 500;'>- Search and filter through insider trading data 	✅</p>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 25px; font-weight: 500;'>- Analyze stock data and performance 	✅</p>", unsafe_allow_html=True)
    st.markdown("<p style=' font-size: 25px; font-weight: 500;'>- Compare insider returns to the S&P 	✅</p>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 25px; font-weight: 500;'>- Selected case studies for more fundamental investment decisions	✅</p>", unsafe_allow_html=True)
    

    # Add space
    st.markdown("<p style='font-size: 30px; font-weight: 625'></p>", unsafe_allow_html=True)
      
    st.markdown("<p style='font-size: 32px; font-weight: 700'>Why is it important to know what insiders are doing?</p>", unsafe_allow_html=True)
   
    ### Add Pelosi Article
    import webbrowser
    col1, col2, col3 = st.columns(3)

    with col1:
        st.write(' ')

    with col2:
      # Add button
          Congress_button = st.button("Example for insider performance")
          if Congress_button:
            webbrowser.open("https://nypost.com/2022/01/07/nancy-pelosi-makes-30-million-from-tech-stocks-scoffs-at-push-to-ban-congressional-trades/")  
          else:
              st.write("")  
              
      # Add Congress Performance        
    st.markdown("<p style='font-size: 25px; font-weight: 500'>Congress members outperform the market</p>", unsafe_allow_html=True)

    with col3:
        st.write(' ')

    # Add congress graph
    col1, col2, col3 = st.columns(3)

    with col1:
        st.image("congress3.png", width = 500)

    with col2:
        st.write(' ')
     
    with col3:   
        Quiver_button = st.button("Checkout Quiver Quantitative")
        if Quiver_button:
            webbrowser.open("https://www.quiverquant.com/strategies/")
     

###
    st.markdown("<p style='font-size: 30px; font-weight: 625'></p>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 30px; font-weight: 575'>InsidersInvest allows you to become an insider yourself!</p>", unsafe_allow_html=True)
    # Add a call-to-action button
    
    
    Try_button = st.button("Try it now")
    if Try_button:
        webbrowser.open("http://localhost:8501/")
            

        
    # # Organize information in a logical structure
    # st.header("General Info on Insider Trading")
    # st.markdown("etc.")
    # st.header("Project Members:")
    # st.markdown("Possiblity for Pictures etc.")

    # st.header("Stock Names & Tickers")

Stocklist = pd.read_excel("Stocklist.xlsx")
StocksnTickers = Stocklist.iloc[1:, [0,1]]
StocksnTickers.columns = ['Ticker', 'Company Name']
    # Add logo
st.sidebar.image("logo_new.png")
    # Add a search box
search_term = st.sidebar.text_input("Ticker or Company Search")

    # Filter the DataFrame based on the search term
filtered_df = StocksnTickers[(StocksnTickers['Company Name'].str.contains(search_term, case=False, na=False)) | (StocksnTickers['Ticker'].str.contains(search_term, case=False, na=False))]

    # Show the filtered DataFrame
with st.sidebar:
    st.dataframe(filtered_df)
        
if __name__ == "__main__":
    main()




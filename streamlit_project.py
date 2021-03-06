#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import pickle

# set page layout
st.set_page_config(
    page_title="Housing Market",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache(allow_output_mutation=True)
def load_data():
    """ Load the cleaned data """
    with open('houses_data.pkl', 'rb') as f:
        df = pickle.load(f)
    
    #df = pd.read_csv("houses_data_v2.csv")
    #try pulling from sql
    #engine = create_engine("sqlite:///sold_houses.db")
    return df


st.title("🏠 Housing Market Dashboard")

houses_data = load_data()


# Calculate the date range for the slider
min_date =  datetime.strptime(min(houses_data["sold_date"].astype(str)), "%Y-%m-%d")
max_date =  datetime.strptime(max(houses_data["sold_date"].astype(str)), "%Y-%m-%d")


st.sidebar.subheader("Inputs")
min_selection, max_selection = st.sidebar.slider("Time Range", min_value=min_date, max_value=max_date, value = [min_date, max_date])

show_state = st.sidebar.checkbox("Show Analysis by State")
select_state = st.sidebar.selectbox('Select a State',sorted(houses_data['state'].unique()))

show_city = st.sidebar.checkbox("Show Analysis by City")
houses_data.city = houses_data.city.astype(str)
select_city = st.sidebar.selectbox('Select a City',sorted(houses_data[houses_data['state'] == select_state]['city'].unique()))


# Toggles for the feature selection in sidebar
show_histograms = st.sidebar.checkbox("Show Histograms")
show_summary = st.sidebar.checkbox("Show Summary Statistics Table")

# Filter Data based on selections
houses_data = houses_data[
    (houses_data["sold_date"] >= min_selection) & (houses_data["sold_date"] <= max_selection)
]
if show_state and show_city:
    ##state
    filtered_data = houses_data[houses_data['state'] == select_state]
    ##city
    filtered_data = filtered_data[filtered_data['city'] == select_city]
elif show_state:
    filtered_data = houses_data[houses_data['state'] == select_state]
elif show_city:
    filtered_data = houses_data[houses_data['city'] == select_city]
else:
    filtered_data = houses_data
st.write(f"Data Points: {len(filtered_data)}")

# Plot the GPS coordinates on the map (need to change column names)
st.map(filtered_data)

# Plot the histograms based on the selections

if show_histograms:
    #Number of sales by property type
    plt.xticks(rotation=180)
    sales = filtered_data.groupby(filtered_data['property_type']).size().sort_values(ascending=False).plot(kind="bar")
    sales.set_xlabel("Property Type")
    hist_sales = sales.get_figure()
    st.subheader("Number of Sales by Property Type")
    st.pyplot(hist_sales)
    
    #Median Price by Property Type
    avg_price= filtered_data.groupby(filtered_data['property_type'])['sold_price'].median().sort_values(ascending=False).plot(kind="bar")
    avg_price.set_xlabel("Property Type")
    avg_price.set_ylabel("Price in $M")
    hist_price = avg_price.get_figure()
    st.subheader("Median Sold Price by Property Type")
    st.pyplot(hist_price)  

if show_summary:
    st.subheader("Summary Table")
    price_sqft = filtered_data['price_sqft'].mean()
    new_const = "{} %".format(round(filtered_data['new_const'].sum()/filtered_data.shape[0]*100,2))
    median_price = "${}".format(int(filtered_data[ 'sold_price'].mean()))
    summary = pd.DataFrame({'Price per Sqft': [price_sqft], '% New Construction': [new_const], 'Median Price Sold': [median_price]} )
    st.table(summary)

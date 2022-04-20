#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# set page layout
st.set_page_config(
    page_title="Housing Market",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache
def load_data():
    """ Load the cleaned data """
    df = pd.read_csv("houses_data_sample.csv")
    #houses_data["sold_date"] = pd.to_datetime(travel_log["ts"])
#     engine = create_engine("sqlite:///sold_houses.db")
#     df = pd.read_sql('SELECT * FROM houses;', engine)
    return df


st.title("🏠 Housing Market Dashboard")

houses_data = load_data()

# Calculate the price range for the slider
min_price = min(houses_data["sold_price"])
max_price = max(houses_data["sold_price"])

# st.sidebar.subheader("Inputs")
# min_selection, max_selection = st.sidebar.slider("Sold Price $", min_value=min_price, max_value=max_price, value = [min_price, max_price])

st.sidebar.checkbox("Show Analysis by State", True, key=1)
select_state = st.sidebar.selectbox('Select a State',sorted(houses_data['state'].unique()))

st.sidebar.checkbox("Show Analysis by City", True, key=1)
select_city = st.sidebar.selectbox('Select a City',sorted(houses_data[houses_data['state'] == select_state]['city'].unique()))


# Toggles for the feature selection in sidebar
show_histograms = st.sidebar.checkbox("Show Histograms")
show_summary = st.sidebar.checkbox("Show Summary Statistics Table")

# Filter Data based on selections
##price
#filtered_data = houses_data[(houses_data["sold_price"] >= min_selection) & (houses_data["sold_price"] <= max_selection)]
##state
filtered_data = houses_data[houses_data['state'] == select_state]
##city
filtered_data = filtered_data[filtered_data['city'] == select_city]

st.write(f"Data Points: {len(filtered_data)}")

# Plot the GPS coordinates on the map (need to change column names)
st.map(filtered_data)

# Plot the histograms based on the selections

if show_histograms:
    #Number of sales by property type
    sales = filtered_data.groupby(filtered_data['property_type']).size().plot(kind="bar")
    sales.set_xlabel("property_type")
    hist_sales = sales.get_figure()
    st.subheader("# Sales Split by Property Type")
    st.pyplot(hist_sales)
    
    #Median Price by Property Type
    avg_price= filtered_data.groupby(filtered_data['property_type'])['sold_price'].median().plot(kind="bar")
    avg_price.set_xlabel("Property Type")
    hist_price = avg_price.get_figure()
    st.subheader("Median Sold Price by Property Type")
    st.pyplot(hist_price)

def new_const(row):
    if row['year_built'] >= 2021:
        return 1
    else:
        return 0    

if show_summary:
    filtered_data['new_const'] = filtered_data.apply(new_const, axis=1)
    st.subheader("Summary Table")
    price_sqft = filtered_data['price_sqft'].mean()
    new_const = "{} %".format(round(filtered_data['new_const'].sum()/filtered_data.shape[0]*100,2))
    median_price = "${}".format(int(filtered_data[ 'sold_price'].mean()))
    summary = pd.DataFrame({'Price per Sqft': [price_sqft], '% New Construction': [new_const], 'Median Price Sold': [median_price]} )
    st.table(summary)


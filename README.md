# Housing Market Dashboard

Current real estate markets have been experiencing increasing prices and bidding wars across the country. Homebuyers need to do their own research to understand market trends and conditions to make informed decisions. While available separately on websites such as Redfin, useful information like average sale price by sqft and by type, average days on the market, average over/under ask are not readily available and aggregated in a user-friendly interface.  

This project aims at building an interactive dashboard to display up-to-date housing market data,summary key statistics and graphs. 

## Data Description
The current dataset is downloaded from Redfin consisting of recently sold houses in more than 1000 different US cities. The data includes different variables obtained from Redfin for each house such as sold price,  sqft and house type. These features are then used to calculate different statistics during the pipeline phase to be displayed in the final dashboard. 

The data downloaded from Redfin however doesn't contain all information presented on the website are is missing some interesting variables such as list price, Redfin estimate and days on the market before sold. So I developed a scraping pipeline to get the individual sold houses urls and scrape this information from each house's page. But the dataset scraped so far is limited and hence not shown in the app. 

## Deployment
All data obtained from Redfin is downloaded and stored in SQL format.The intent would be to update/augment this data on a regular basis. Some data cleaning and processing is then performed on the data before using it in the [final dashboard](https://share.streamlit.io/salmakatri/ide-project/main/streamlit_project.py) with Streamlit. This app allows user to interact with the data to customize the view by location, price range and sold date to see key statitics. As data size and period covered grows, more trend analysis can also be added to the dashboard. 


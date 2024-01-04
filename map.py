import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import geopandas as gpd
import plotly.express as px

# read in data and drop columns that are unnecessary
data = pd.read_csv("meteorite-landings.csv")
data = data.drop(labels = ["name","id","nametype","recclass","mass"], axis = 1)

# get rid of the wrong years and no values with no geolocation
data = data.loc[(data["year"] >= 860) & (data["year"] <= 2016)]
data = data[(data["reclat"] != 0.0) & (data["reclong"] != 0.0)]


# drop data with missing values
data = data.dropna(axis = 0, how = "any")

# printing out values to check values are correct
data.info()
data.shape
print(data)

# Defining what colour is associated with types of meteorite falls vs finds
color_discrete_map = {"Observed meteorite falls": "coral", "Unobserved meteorite falls": "cornflowerblue"}


# Create scatter plot map 
fig = px.scatter_geo(data, lat='reclat', lon='reclong', color='Location of found meteorites', opacity = 1, color_discrete_map = color_discrete_map,
                     hover_name='year',
                     title='Found Meteorite Locations - Observed Fall vs Unobserved Fall')

# changing the size of the markers
fig.update_traces(marker=dict(size=4,),
                  selector=dict(mode='markers'))

# changes fontsize 
fig.update_layout(
    title={'text': 'Found Meteorite Locations - Observed Fall vs Unobserved Fall', 'font': {'size': 20}},
    legend={'font': {'size': 15}}
)

# makes points in legend a constant size that is not dependent on size of points on map
fig.update_layout(legend= {'itemsizing': 'constant'})

# show figure
fig.show()

import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import geopandas as gpd
import plotly.express as px
import math

# read in data and drop unnecessary labels
data = pd.read_csv("meteorite-landings.csv")
data = data.drop(labels = ["name","id","nametype","recclass","mass"], axis = 1)


# get rid of the wrong years, no geolocation data points, and leaving only observed falls
data = data.loc[(data["year"] >= 860) & (data["year"] <= 2000)]
data = data[(data["reclat"] != 0.0) & (data["reclong"] != 0.0)]
data = data[(data["Location of found meteorites"] != "Unobserved meteorite falls")]


# drop data with missing values
data = data.dropna(axis = 0, how = "any")

# test if values are correct by printing out the values
data.info()
data.shape
print("DATA SHAPE:",  data.shape[0])
print(data)

# changing each year to the upper half a century, i.e. 1944 = 1950
data["year"] = data["year"].apply(lambda x: math.ceil(x / 50) * 50)

# test if values are correct by printing out the values
data.info()
data.shape
print(data)    

# setting a colour value to the type of meteortie fall
color_discrete_map = {"Observed meteorite falls": "coral"}


# Create dynamic scatter map
fig = px.scatter_geo(data, lat='reclat', lon='reclong', animation_frame = "year", color='Location of found meteorites', opacity = 1, color_discrete_map = color_discrete_map,
                     hover_name='year', title='Locations of Observed Meteorites')

# changing the size of the markers
fig.update_traces(marker=dict(size=4),
                  selector=dict(mode='markers'))

# changing legend and title sizes
fig.update_layout(
    title={'text': 'Locations of Observed Falling Meteorites That Were Later Found (from 900 CE to 2000 CE over 50 year increments)', 'font': {'size': 20}},
    legend={'font': {'size': 15}}
)

# makes points in legend a constant size that is not dependent on size of points on map
fig.update_layout(legend= {'itemsizing': 'constant'})

# changing speed of dynamic map
fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 1000
fig.write_html("dynamic_map.html")
fig.show()

import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import geopandas as gpd
import csv

# read in data and drop unnecessary headings
data = pd.read_csv("meteorite-landings.csv")
data = data.drop(labels = ["name","id","nametype","recclass"], axis = 1)
# data['mass']

#%%
# get rid of the wrong years and meteorites with 0 mass
data = data.loc[(data["year"] >= 860) & (data["year"] <= 2016)]
data = data[(data["mass"] != 0.0)]


# calculates the mean values of the mass column grouped by the "Location of found meteorites" column, only including numeric values
mean_mass = data.groupby("Location of found meteorites")["mass"].mean(numeric_only = True)
# testing mean mass is correct
print(mean_mass)

# Create bar graph
x_axis = ['Observed meteorite falls', 'Unobserved meteorite falls']
y_axis = [mean_mass[0], mean_mass[1]]

colors = ['coral', 'cornflowerblue']
plt.bar(x_axis, y_axis, color = colors)

# set title names and font sizes
plt.title('Mean Mass of Found Meteorites - Observed vs Unobserved Falls \n', fontsize = 20)
# plt.xlabel('Observed vs Unobserved Meteorite Falls', fontsize = 14)
plt.ylabel('Meteorite Mass (grams) \n', fontsize = 15)

plt.xticks(fontsize=15)  # Adjust font size here
plt.yticks(fontsize=15)  
# show graph
plt.show()

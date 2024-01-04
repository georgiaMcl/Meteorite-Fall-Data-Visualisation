import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import geopandas as gpd
import plotly.express as px
import requests
from geopy.geocoders import Nominatim
import pandas as pd
import reverse_geocoder
import csv
import reverse_geocoder

# read in file
data = pd.read_csv("meteorite-landings.csv")
data = data.drop(labels = ["name","id","nametype","recclass","mass"], axis = 1)


# get rid of the wrong years, no geolocation data points, and leaving only meteorite falls
data = data.loc[(data["year"] >= 860) & (data["year"] <= 2016)]
data = data[(data["reclat"] != 0.0) & (data["reclong"] != 0.0)]
data = data[(data["Location of found meteorites"] != "Unobserved meteorite falls")]


# drop data with missing values
data = data.dropna(axis = 0, how = "any")


def get_country_from_coordinates(coordinate):
    # get country code from coordinates
    result = reverse_geocoder.search([coordinate])
    
    if result:
        country = result[0]['cc']
        return country
    else:
        return "Unknown"


# creates a new column and puts the value "Japan" as all values (Japan is just an arbitrary value)
data['country'] = "Japan"

def main():
    # create a list to hold all country codes
    countries = []
    input_csv = "meterorite_landings_test.csv"

    # iterate through each row and get country code for each meteorite coordinte
    for index, row in data.iterrows():
        Latitude = row["reclat"]
        Longitude = row["reclong"]
        location = get_country_from_coordinates((Latitude,Longitude))
        
        data.to_csv("meterorite_landings_test.csv", index=False)
        # append this new country code to the country code list
        countries.append(location)
        # test to see if it is working by printing out the values
        print(location)
    
    # set the country column to equal the list of country codes
    data['country'] = countries
    # create a new csv file with this new column and save it so as to not update the old data
    data.to_csv("meteorite_landings_with_country.csv", index=False)
    # check data is correct by printing values
    print(data)
        
if __name__ == "__main__":
    main()

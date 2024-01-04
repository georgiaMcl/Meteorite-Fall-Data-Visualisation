import pandas as pd
import pycountry_convert as pc
# read in csv file
data = pd.read_csv("meteorite_landings_with_country.csv")

# creates a new column and puts the value "Antartica" as all values ("Antartica" is just an arbitrary value)
data["continent"] = "Antartica"

# createss a list to hold the continent names
continents = []

# funciton that contains a dictionary of all continent codes and their respective continent names
def get_continent_name(continent_code: str) -> str:
    continent_dict = {
        "NA": "North America",
        "SA": "South America",
        "AS": "Asia",
        "AF": "Africa",
        "OC": "Oceania",
        "EU": "Europe",
        "AQ" : "Antarctica"
    }
    return continent_dict[continent_code]

# iterate through every meteorite to get the conintnent name from the respective country code.
for index, row in data.iterrows():
    country = row["country"]
    if pd.notna(country):  # Check for NaN values
        # Get continent code from country code
        continent = pc.country_alpha2_to_continent_code(country)
        # Get continent name from continent code
        continent_name = get_continent_name(continent)
        # append the coninent name to the list of coninents
        continents.append(continent_name)
    else:
        continents.append("Unknown")  # Handle missing country values

# set the continent column to equal the continent list
data['continent'] = continents
# create a new csv file with this new column and save it so as to not update the old data
data.to_csv("meteorite_landings_with_continent.csv", index=False)
print(data)
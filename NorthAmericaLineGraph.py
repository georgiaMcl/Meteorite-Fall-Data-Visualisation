import pandas as pd
from matplotlib import pyplot as plt
import math

# read in data
continent_data = pd.read_csv("meteorite_landings_with_continent.csv")
population_data = pd.read_csv("population.csv")

# making all years in 50 year increments
continent_data["year"] = continent_data["year"].apply(lambda x: math.ceil(x / 50) * 50)

# as 2000 - 2016 will not have 50 years worth of data it will be less than expected, remove this outlier by making years < 2001
continent_data = continent_data.loc[(continent_data["year"] <2001)]

# test year values are correct by printing values
print("continent data rounded years: ", continent_data)


# create a list of years
start = 900
end = 2000
step = 50
years_list = [i for i in range(start, end + 1, step)]

# test values are correct by printing values
print("Years list", years_list)

# Ensuring we only get North America related data
continent_data = continent_data[continent_data["continent"] == "North America"] 
population_data = population_data[population_data["Entity"] == "North America"] 

# Ensure that population data only has the data for every 50 years
population_data = population_data[population_data["Year"].isin(years_list)]

# Create a new DataFrame with all years from years_list
all_years_data = pd.DataFrame({"Year": years_list})

# Merge the filtered data with all_years_data and fill missing values with 0
merged_data_population = all_years_data.merge(population_data, on="Year", how="left").fillna(0)

# averages the population values between two surrounding years for the years where there is no data
population_list = []
for i in range(0, len(merged_data_population["Population"] + 1)):
    if merged_data_population["Population"][i] == 0:
        this_years_pop = (merged_data_population["Population"][i - 1] + merged_data_population["Population"][i + 1])/2
        population_list.append(this_years_pop)
    else:
        population_list.append(merged_data_population["Population"][i])

# testing population values are correct by printing values
print("population_list: ", population_list)     

# change population values to be in terms of million, e.g. value 80 on graph means 80 million
for i in range(0, len(merged_data_population["Population"] + 1)):
    population_list[i] = population_list[i]/1000000

# testing population converstion to millions is correct by printing values
print("population_list after converstion to millions: ", population_list)

# create list of number of meteorites every 50 years
number_of_meteorite_falls = [0] * ((2000 - 900) // 50 + 1)

# test the list contains enough elements for all the years by printing the list
print("the number of meteorite falls unpopulated list: ", number_of_meteorite_falls)

# Updates list to check if the year appears for a meteorite, if it does, we increment that value in its corresponding year slot, i.e. if two meteorites fell in 1950 then the 1950 spot will have the value 2
for index, row in continent_data.iterrows():
    year = row["year"]
    interval_index = (year - 900) // 50
    number_of_meteorite_falls[interval_index] += 1

# test number of meteorite falls in list is correct by printing value
print(number_of_meteorite_falls)

# set first y axis to the population list
y_coord_pop = population_list
# test values are correct by printing values
print("y_coord_pop: ", y_coord_pop)

# set x value and second y axis to number of meteorite falls list
x_coord = years_list
y_coord_meteorite = number_of_meteorite_falls 

# create figure
fig,ax = plt.subplots()

# left y-axis figure
ax.plot(x_coord, y_coord_pop, color = 'darkseagreen', linestyle = 'dashed',
         marker = 'o')
ax.set_xlabel("Year (CE)", fontsize = 14)
ax.set_ylabel("Human Population of North America (millions)", color = "darkseagreen", fontsize = 14)

# creating right y-axis
ax2 = ax.twinx()
ax2.plot(x_coord,y_coord_meteorite , color="coral",marker="o")
ax2.set_ylabel("Number of Found Meteorites With Fall Observations in North America",color="coral",fontsize=14)
fig.suptitle('North America - Human Population With Number of Observed Falling Meteorites That Were Later Found (from 900 CE to 2000 CE over 50 year increments)', fontsize = 14)
plt.show()



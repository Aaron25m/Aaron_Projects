#!/usr/bin/env python
# coding: utf-8

# In[378]:


import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt


# In[379]:


df=pd.read_csv("turkey_earthquakes(1915-2021).csv",delimiter=";")
del df["No"]
df = df.rename(columns={'Deprem Kodu': 'Code', 'Olus tarihi': 'Date', 'Olus zamani': 'Time','Enlem':'Latitude','Boylam':'Longitude','Derinlik':'Depth','xM':'Magnitude','Yer':'Location'})
del df["Code"],df["Tip"],df["MD"],df["ML"],df["Mw"],df["Ms"],df["Mb"]
df.columns


# In[380]:


df=df.iloc[::-1].reset_index(drop=True)


# In[381]:


df.info()


# In[422]:


pd.DataFrame(df.groupby(df['Location'])['Magnitude'].median().sort_values(ascending=False).head(7))


# In[430]:


df['Date'] = pd.to_datetime(df['Date'])

# Extract year from date column and create a new column
df['month'] = df['Date'].dt.month
df['month'].value_counts()


# In[444]:


min_mag = 3
max_mag = 4.5
step=0.01
for mag in np.arange(min_mag,max_mag+step):
    mag_earthquakes = df.loc[df["Magnitude"] == mag] 
# Group earthquakes by year 
    year_groups = mag_earthquakes.groupby("Year") 
    year_counts = year_groups.size()  
    percent_increase = year_counts.pct_change() * 100 
# Print the percentage increase for each year 
    print(f"Percentage increase of {mag}+ magnitude earthquakes:") 
    #print(percent_increase) 

fig, ax = plt.subplots()


ax.plot(percent_increase.index, percent_increase, label=f"{mag:.1f}+ magnitude")

# Set axis labels and legend
ax.set_xlabel("Year")
ax.set_ylabel("Percentage Increase")
ax.legend()

# Show the plot
plt.show()


# In[435]:


# Temporal analysis
percent_increase.groupby('Year').size().plot(kind='line')
plt.xlabel('Year')
plt.ylabel('Number of earthquakes')
plt.show()


# In[452]:


pd.DataFrame(df.groupby(df['Location'])['Magnitude'].median().sort_values(ascending=False).head(7))


# In[465]:


df[df.apply(lambda row: row.astype(str).str.contains('KURUTILEK').any(), axis=1)]


# In[9]:


import pandas as pd
import folium
from folium.plugins import HeatMap

# Load the data into a pandas dataframe
# Create a map centered on Turkey
turkey_map = folium.Map(location=[39.9334, 32.8597], zoom_start=5)

# Add a heat map layer to the map
heat_data = [[row['Latitude'], row['Longitude'], row['Magnitude']] for index, row in df.iterrows()]
HeatMap(heat_data, min_opacity=0.2, max_val=max(df['Magnitude']), radius=10, blur=7, max_zoom=1).add_to(turkey_map)

# Display the map
turkey_map


# In[386]:


data=pd.read_csv("dataturk.csv")
import pandas as pd
import folium
from folium.plugins import HeatMap
data['mag'] = data['mag'].astype(float)

# replace NaN values with 0.0
data['mag'].replace(np.nan, 0.0, inplace=True)
# Load the data into a pandas dataframe
# Create a map centered on Turkey
turkey_map = folium.Map(location=[39.9334, 32.8597], zoom_start=5)

# Add a heat map layer to the map
heat_data = [[row['lat'], row['long'], row['mag']] for index, row in data.iterrows()]
HeatMap(heat_data, min_opacity=0.2, max_val=max(data['mag']), radius=10, blur=7, max_zoom=1).add_to(turkey_map)

# Display the map
turkey_map


# In[427]:


data=pd.read_csv("dataturk.csv")
plt.hist(data['mo'], bins=20)
plt.xlabel('Magnitude')
plt.ylabel('Frequency')
plt.show()
#pd.DataFrame(data.groupby(data['location'])['mag'].median().sort_values(ascending=False).head(7))


# In[476]:


import matplotlib.pyplot as plt

# drop rows with missing values
df = data[['Year', 'Deaths']].dropna()

# group the data by year and sum the number of houses destroyed in each year
houses_destroyed_by_year = df.groupby('Year').sum().reset_index()

# create a line plot of houses destroyed by year using Matplotlib
plt.plot(houses_destroyed_by_year['Year'], houses_destroyed_by_year['Deaths'])
plt.title('Deaths by Year')
plt.xlabel('Year')
plt.ylabel('Deaths occured')
plt.show()


# In[474]:


import plotly.express as px

data = pd.read_csv('dataturk2.tsv', delimiter='\t')
data['Deaths'] = data['Deaths'].fillna(0)
data['Houses Destroyed'] = data['Houses Destroyed'].fillna(0)
data = data.drop(columns=['Search Parameters', 'Vol', 'Missing','Missing Description','Total Missing','Total Missing Description','Tsu','Total Death Description','Total Injuries Description','Total Damage Description','Total Houses Destroyed Description','Total Houses Damaged Description'])
data = data.drop(columns=['Death Description','Injuries Description', 'MMI Int','Houses Destroyed Description','Total Injuries','Houses Damaged Description','Total Houses Destroyed','Total Houses Damaged'])
data = data.drop(columns=['Total Deaths'])
data=data.drop(columns=['Hr','Mn','Sec'])
data=data.drop(columns=['Houses Damaged'])
df = data[['Year', 'Deaths']]

# drop rows with missing values
df = df[['Year', 'Deaths']]

# drop rows with missing values
df = df.dropna()

# group the data by year and sum the number of deaths in each year
deaths_by_year = df.groupby('Year').sum().reset_index()

# create a line plot of deaths by year using Plotly
fig = px.line(deaths_by_year, x='Year', y='Deaths', title='Number of Deaths by Year')

# display the plot
fig.show()


# In[374]:


data


# In[470]:


import pandas as pd
import matplotlib.pyplot as plt


# Magnitude distribution analysis
plt.hist(df['Magnitude'], bins=20)
plt.xlabel('Magnitude')
plt.ylabel('Frequency')
plt.show()

# Temporal analysis
df['Date'] = pd.to_datetime(df['Date'])
df['Year'] = df['Date'].dt.year
df.groupby('Year').size().plot(kind='line')
plt.xlabel('Year')
plt.ylabel('Number of earthquakes')
plt.show()

# Spatial analysis
plt.scatter(df['Longitude'], df['Latitude'], s=df['Magnitude'])
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.show()

# Correlation analysis
df.plot.scatter(x='Depth', y='Magnitude',)
plt.xlabel('Magnitude')
plt.ylabel('Depth')
plt.show()


# In[405]:


# Filter earthquakes with magnitude less than 4.5
df_filtered = df[df['Magnitude'] < 4.5]

# Extract year from date column and create a new column
df_filtered['Year'] = df_filtered['Date'].dt.year

# Group the filtered DataFrame by year and magnitude, and count the number of earthquakes
grouped = df_filtered.groupby(['Year', 'Magnitude']).size().reset_index(name='Count')

# Pivot the grouped DataFrame to create a pivot table with year as index and magnitude as columns
pivot_table = pd.pivot_table(grouped, values='Count', index='Year', columns='Magnitude', fill_value=0)

# Plot the pivot table as a line chart
pivot_table.plot(kind='line')

# Add labels and title to the plot
plt.xlabel('Year')
plt.ylabel('Number of Earthquakes')
plt.title('Earthquakes with Magnitude < 4.5 by Year')

# Show the plot
plt.show()


# In[11]:


huge_quakes = df[df['Magnitude'] >= 7]

# count number of huge earthquakes
num_huge_quakes = len(huge_quakes)

print(f'{num_huge_quakes} huge earthquakes have occurred.')


# In[19]:


import pandas as pd


# filter earthquakes with magnitude greater than or equal to 5
large_quakes = df[df['Magnitude'] >= 6]

# convert Date column to datetime format using .loc
large_quakes.loc[:, 'Date'] = pd.to_datetime(large_quakes['Date'])

# compute time between events in months using .loc
time_between = (large_quakes.loc[:, 'Date'].diff() / pd.Timedelta(days=30)).dropna()

# compute mean time between events in months
mean_time_between = time_between.mean()

# store dates of earthquakes above 5 MW in a list
quake_dates = large_quakes['Date'].tolist()

# compute average time between consecutive dates in months
avg_time_between_dates = sum((quake_dates[i+1] - quake_dates[i]).days for i in range(len(quake_dates)-1)) / (len(quake_dates)-1) / 30

print(f'Earthquakes above 5 MW occur on average every {mean_time_between:.2f} months.')
print(f'Dates of earthquakes above 5 MW: {quake_dates}')
print(f'Average time between consecutive dates: {avg_time_between_dates:.2f} months')


# In[21]:


min_lat, max_lat = 36, 42
min_lon, max_lon = 26, 45

# select quakes that occurred within the boundaries of the Anatolian plate
anatolian_quakes = df[(df['Latitude'] >= min_lat) & (df['Latitude'] <= max_lat) & 
                      (df['Longitude'] >= min_lon) & (df['Longitude'] <= max_lon)]

# count the number of earthquakes in each location
quake_counts = anatolian_quakes['Location'].value_counts()

# print the respective amount of earthquakes for each location
for loc, count in quake_counts.iteritems():
    print(f"{loc}: {count} earthquakes")


# In[43]:


import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# Load the earthquake data from a CSV file


# Split the date column into year, month, and day columns
df['Year'] = df['Date'].str.split('.').str[0].astype(int)
df['Month'] = df['Date'].str.split('.').str[1].astype(int)
df['Day'] = df['Date'].str.split('.').str[2].astype(int)

# Preprocess the location column using one-hot encoding
location_encoder = OneHotEncoder()
transformer = ColumnTransformer([('location_encoder', location_encoder, ['Location'])], remainder='passthrough')
X = transformer.fit_transform(df[['Location', 'Latitude', 'Longitude']])
y = df['Magnitude']

# Train a linear regression model to predict the magnitude of earthquakes
model = LinearRegression()
model.fit(X, y)

# Define new locations for which to predict earthquake magnitudes
new_locations = pd.DataFrame({
    'Location': ['AZERBAYCAN'],
    'Latitude': [44.5],
    'Longitude': [40.5],
})

# Use the trained model to predict the magnitudes of earthquakes at the new locations
new_X = transformer.transform(new_locations)
new_y = model.predict(new_X)

# Print the predicted magnitudes for each location
for i, location in enumerate(new_locations['Location']):
    print(f"Next earthquake in {location} will be of magnitude {new_y[i]:.2f}")


# In[97]:


words = df['Location'].str.split()

# create an empty list to store words that start with "h"
h_words = []

# iterate over each word and check if it starts with "h"
for word in words:
    for w in word:
        if w.startswith('DUZCE'):
            h_words.append(w)

# print the list of words that start with "h"
print(h_words)


# In[98]:


df[df['Location'] =='DUZCE-SEFERIHISAR']


# In[107]:


import plotly.express as px

# Create a dataframe of the top 5 hit regions and their frequency based on the earthquake magnitude
top_regions = df.groupby('Location')['Magnitude'].count().nlargest(5).reset_index(name='Frequency')

# Create the horizontal bar graph using Plotly
fig = px.bar(top_regions, x='Frequency', y='Location', orientation='h',
             color='Frequency', title='Top 5 Regions with the Most Frequent Earthquakes',
             labels={'Frequency': 'Frequency of Earthquakes', 'Location': 'Region'})

fig.show()


# In[122]:




# Convert the Date column to a datetime object
df['Date'] = pd.to_datetime(df['Date'])

# Filter earthquakes above magnitude 5
df = df[df['Magnitude'] >= 5]

# Group the earthquakes into magnitude bins
bins = [5, 5.9, 6.9, 7.9, 8.9, 9.9]
labels = ['5-5.9', '6-6.9', '7-7.9', '8-8.9', '9-9.9']
df['Magnitude Bin'] = pd.cut(df['Magnitude'], bins=bins, labels=labels)

# Group the earthquakes by decade and magnitude bin
df['Decade'] = df['Date'].dt.year // 10 * 10
grouped = df.groupby(['Decade', 'Magnitude Bin']).size().reset_index(name='Count')

# Plot the trend of earthquakes by decade and magnitude bin
fig = px.line(grouped, x='Decade', y='Count', color='Magnitude Bin',
              labels={'Decade': 'Decade (1900s-2010s)', 'Count': 'Earthquake Count'})
fig.update_layout(title='Trend of Earthquakes by Magnitude Bin and Decade')
fig.show()


# In[132]:


import pandas as pd
import plotly.express as px


# Define a function to assign a direction based on latitude and longitude
def assign_direction(row):
    if row['Longitude'] < 35:
        return 'West'
    elif row['Longitude'] > 45:
        return 'East'
    elif row['Latitude'] < 38:
        return 'South'
    else:
        return 'North'

# Add a new column 'Direction' to the dataframe
df['Direction'] = df.apply(assign_direction, axis=1)

# Group the data by direction and magnitude, and count the number of earthquakes in each group
grouped = df[df['Magnitude'] >= 5].groupby(['Direction', pd.cut(df[df['Magnitude'] >= 5]['Magnitude'], [5, 6, 7, 8, 9, 10]).astype(str)]).size().reset_index(name='count')

# Plot a graph of Direction vs Magnitude
fig = px.bar(grouped, x='Magnitude', y='count', color='Direction', barmode='group', title='Earthquakes by Direction and Magnitude')
fig.show()


# In[147]:


len(df)


# In[151]:



len(df)

# Calculate the percentage of earthquakes over 6 magnitude in Turkey
percentage = len(df[df['Magnitude'] >= 6])/len(df) * 100

print(f"{percentage:.2f}% of earthquakes with magnitude over 6 occurred in Turkey.")


# In[154]:



len(df)

# Calculate the percentage of earthquakes over 6 magnitude in Turkey
percentage = len(df[df['Magnitude'] <= 4.5])/len(df) * 100

print(f"{percentage:.2f}% of earthquakes with magnitude less than 4.5 occurred in Turkey.")


# In[161]:


import pandas as pd
import plotly.express as px


# Distribution of earthquake depths
fig1 = px.histogram(df, x='Depth', nbins=20, title='Distribution of Earthquake Depths')
fig1.show()

# Correlation between magnitude and depth
fig2 = px.scatter(df, x='Magnitude', y='Depth', title='Magnitude vs Depth', trendline='ols')
fig2.show()

# Depth vs location
fig3 = px.scatter_mapbox(df, lat='Latitude', lon='Longitude', hover_name='Depth', zoom=5, title='Depth vs Location')
fig3.show()

# Depth over time
df['Date'] = pd.to_datetime(df['Date'])
fig4 = px.line(df, x='Date', y='Depth', title='Depth Over Time')
fig4.show()


# In[471]:


import matplotlib.pyplot as plt

# Create a new dataframe with the columns 'Date' and 'Depth'
depth_df = df[['Date', 'Depth']]

# Convert the 'Date' column to a datetime object
depth_df['Date'] = pd.to_datetime(depth_df['Date'])

# Group the dataframe by year and calculate the mean depth for each year
depth_by_year = depth_df.groupby(depth_df['Date'].dt.year).mean()

# Create the plot using Matplotlib
plt.plot(depth_by_year.index, depth_by_year['Depth'])
plt.title('Depth of Earthquakes over Time')
plt.xlabel('Year')
plt.ylabel('Depth')
plt.show()


# In[473]:


import matplotlib.pyplot as plt

# Define the properties of the box
boxprops = dict(linestyle='-', linewidth=2.5, color='blue')

# Create a box plot of earthquake depths with the desired color
plt.boxplot(df['Depth'], boxprops=boxprops)
plt.title('Box Plot of Earthquake Depths')
plt.ylabel('Earthquake Depth')
plt.show()


# In[156]:


import plotly.express as px

# Define the bins for the earthquake magnitudes
bins = [0, 4.5, 5.5, 6.5, 7.5, 10]

# Create a new column 'Magnitude Group' based on the bins
df['Magnitude Group'] = pd.cut(df['Magnitude'], bins, labels=['<4.5', '4.5-5.5', '5.5-6.5', '6.5-7.5', '7.5+'])

# Calculate the percentage of earthquakes in each magnitude group
counts = df.groupby('Magnitude Group').size()
percentages = counts / counts.sum() * 100

# Create a pie chart
fig = px.pie(values=percentages, names=percentages.index, title='Percentage of Earthquakes by Magnitude Group in Turkey')

# Set font size and color
fig.update_layout(
    font=dict(size=16, color='black'),
    title=dict(font=dict(size=20, color='black'))
)

# Add labels to the pie chart
fig.update_traces(textinfo='percent+label')

# Show the plot
fig.show()


# In[75]:


import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# Load the earthquake data from a CSV file
df=pd.read_csv("turkey_earthquakes(1915-2021).csv",delimiter=";")
del df["No"]
df = df.rename(columns={'Deprem Kodu': 'Code', 'Olus tarihi': 'Date', 'Olus zamani': 'Time','Enlem':'Latitude','Boylam':'Longitude','Derinlik':'Depth','xM':'Magnitude','Yer':'Location'})
del df["Code"],df["Tip"],df["MD"],df["ML"],df["Mw"],df["Ms"],df["Mb"]

df=df.iloc[::-1].reset_index(drop=True)
# Split the date column into year, month, and day columns
df['Year'] = df['Date'].str.split('.').str[0].astype(int)
df['Month'] = df['Date'].str.split('.').str[1].astype(int)
df['Day'] = df['Date'].str.split('.').str[2].astype(int)

# Preprocess the location column using one-hot encoding
location_encoder = OneHotEncoder()
transformer = ColumnTransformer([('location_encoder', location_encoder, ['Location'])], remainder='passthrough')
X = transformer.fit_transform(df[['Location', 'Latitude', 'Longitude', 'Year', 'Month']])
y = df['Magnitude']

# Train a linear regression model to predict the magnitude of earthquakes
model = LinearRegression()
model.fit(X, y)

# Define new locations for which to predict earthquake magnitudes
new_locations = pd.DataFrame({
    'Location': ['AKDENIZ'],
    'Latitude': [36],
    'Longitude': [26],
    'Year': [2023],
    'Month': [2]
})

# Use the trained model to predict the magnitudes of earthquakes at the new locations
new_X = transformer.transform(new_locations)
new_y = model.predict(new_X)

# Print the predicted magnitudes for each location
for i, location in enumerate(new_locations['Location']):
    month = int(new_locations.iloc[i]['Month'])
    year = int(new_locations.iloc[i]['Year'])
    print(f"Next earthquake in {location} in {month}/{year} will be of magnitude {new_y[i]:.2f}")


# In[104]:


import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# Load the earthquake data from a CSV file
df=pd.read_csv("turkey_earthquakes(1915-2021).csv",delimiter=";")
del df["No"]
df = df.rename(columns={'Deprem Kodu': 'Code', 'Olus tarihi': 'Date', 'Olus zamani': 'Time','Enlem':'Latitude','Boylam':'Longitude','Derinlik':'Depth','xM':'Magnitude','Yer':'Location'})
del df["Code"],df["Tip"],df["MD"],df["ML"],df["Mw"],df["Ms"],df["Mb"]

df=df.iloc[::-1].reset_index(drop=True)
# Split the date column into year, month, and day columns
df['Year'] = df['Date'].str.split('.').str[0].astype(int)
df['Month'] = df['Date'].str.split('.').str[1].astype(int)
df['Day'] = df['Date'].str.split('.').str[2].astype(int)

# Preprocess the location column using one-hot encoding
location_encoder = OneHotEncoder()
transformer = ColumnTransformer([('location_encoder', location_encoder, ['Latitude', 'Longitude'])], remainder='passthrough')
X = transformer.fit_transform(df[['Latitude', 'Longitude', 'Year', 'Month']])
y = df['Magnitude']

# Train a linear regression model to predict the magnitude of earthquakes
model = LinearRegression()
model.fit(X, y)

# Define new locations for which to predict earthquake magnitudes
new_locations = pd.DataFrame({
    'Latitude': [40.8],
    'Longitude': [31.1],
    'Year': [2022],
    'Month': [11]
})

# Use the trained model to predict the magnitudes of earthquakes at the new locations
new_X = transformer.transform(new_locations)
new_y = model.predict(new_X)

# Print the predicted magnitudes for each location
for i in range(len(new_locations)):
    lat = new_locations.iloc[i]['Latitude']
    long = new_locations.iloc[i]['Longitude']
    month = int(new_locations.iloc[i]['Month'])
    year = int(new_locations.iloc[i]['Year'])
    print(f"Next earthquake at latitude {lat} and longitude {long} in {month}/{year} will be of magnitude {new_y[i]:.2f}")


# In[102]:


import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from geopy.distance import geodesic

# Load the earthquake data from a CSV file
df=pd.read_csv("turkey_earthquakes(1915-2021).csv",delimiter=";")
del df["No"]
df = df.rename(columns={'Deprem Kodu': 'Code', 'Olus tarihi': 'Date', 'Olus zamani': 'Time','Enlem':'Latitude','Boylam':'Longitude','Derinlik':'Depth','xM':'Magnitude','Yer':'Location'})
del df["Code"],df["Tip"],df["MD"],df["ML"],df["Mw"],df["Ms"],df["Mb"]

df=df.iloc[::-1].reset_index(drop=True)
# Split the date column into year, month, and day columns
df['Year'] = df['Date'].str.split('.').str[0].astype(int)
df['Month'] = df['Date'].str.split('.').str[1].astype(int)
df['Day'] = df['Date'].str.split('.').str[2].astype(int)

# Preprocess the location column using one-hot encoding
location_encoder = OneHotEncoder()
transformer = ColumnTransformer([('location_encoder', location_encoder, ['Latitude', 'Longitude'])], remainder='passthrough')
X = transformer.fit_transform(df[['Latitude', 'Longitude', 'Year', 'Month']])
y = df['Magnitude']

# Train a linear regression model to predict the magnitude of earthquakes
model = LinearRegression()
model.fit(X, y)

# Define new locations for which to predict earthquake magnitudes
lat = 40.83
long = 31.16
radius = 1 # in degrees
year=2022
month=11
new_locations = pd.DataFrame({
    'Latitude': [lat],
    'Longitude': [long],
    'Year': [year],
    'Month': [month]
})
for i in range(df.shape[0]):
    dist = geodesic((df.loc[i, 'Latitude'], df.loc[i, 'Longitude']), (lat, long)).km
    if dist <= radius:
        new_locations = new_locations.append(df.loc[i, ['Latitude', 'Longitude', 'Year', 'Month']])
        
# Use the trained model to predict the magnitudes of earthquakes at the new locations
new_X = transformer.transform(new_locations)
new_y = model.predict(new_X)

# Print the predicted magnitudes for each location
for i in range(len(new_locations)):
    lat = new_locations.iloc[i]['Latitude']
    long = new_locations.iloc[i]['Longitude']
    month = int(new_locations.iloc[i]['Month'])
    year = int(new_locations.iloc[i]['Year'])
    print(f"Next earthquake at latitude {lat} and longitude {long} in {month}/{year} will be of magnitude {new_y[i]:.2f}")


# In[170]:


import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA

# Load data into a pandas DataFrame

# Convert date column to datetime format
df['Date'] = pd.to_datetime(df['Date'])

# Set date as index
df.set_index('Date', inplace=True)

# Plot time series data
plt.plot(df['Magnitude'])

# Fit ARIMA model
model = ARIMA(df['Magnitude'], order=(1, 1, 1))
results = model.fit()

# Print summary of model results
print(results.summary())


# In[322]:


import pandas as pd
import numpy as np
import statsmodels.api as sm
from sklearn.ensemble import RandomForestRegressor


data=pd.read_csv("turkey_earthquakes(1915-2021).csv",delimiter=";")
del data["No"]
data = data.rename(columns={'Deprem Kodu': 'Code', 'Olus tarihi': 'Date', 'Olus zamani': 'Time','Enlem':'Latitude','Boylam':'Longitude','Derinlik':'Depth','xM':'Magnitude','Yer':'Location'})
del data["Code"],data["Tip"],data["MD"],data["ML"],data["Mw"],data["Ms"],data["Mb"]
data=data.iloc[::-1].reset_index(drop=True)

# Preprocess data
data["Date"] = pd.to_datetime(data["Date"])
data["Year"] = data["Date"].dt.year
data["Month"] = data["Date"].dt.month
data = data[["Year", "Month", "Magnitude"]]

# Train model
X = data.drop("Magnitude", axis=1)
y = data["Magnitude"]
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

# Generate predictions for every month in 2023
months = pd.date_range(start="2024-01-01", end="2024-12-31", freq="M")
predictions = []
for month in months:
    year = month.year
    month = month.month
    prediction = model.predict([[year, month]])
    predictions.append(prediction[0])

# Calculate probability of earthquakes above 7.5 magnitude for each month in 2023
# Calculate probability of earthquakes above 7.5 magnitude for each month in 2023
threshold = 7.8
probabilities = 1 - (1 / (1 + np.exp(np.array(predictions) - threshold)))

# Print results
for i, month in enumerate(months):
    print(f"{month}: {probabilities[i]:.2%}")


# In[316]:


import pandas as pd
import numpy as np
import statsmodels.api as sm
from sklearn.ensemble import RandomForestRegressor

data=pd.read_csv("turkey_earthquakes(1915-2021).csv",delimiter=";")
del data["No"]
data = data.rename(columns={'Deprem Kodu': 'Code', 'Olus tarihi': 'Date', 'Olus zamani': 'Time','Enlem':'Latitude','Boylam':'Longitude','Derinlik':'Depth','xM':'Magnitude','Yer':'Location'})
del data["Code"],data["Tip"],data["MD"],data["ML"],data["Mw"],data["Ms"],data["Mb"]
data=data.iloc[::-1].reset_index(drop=True)

# Preprocess data
data["Date"] = pd.to_datetime(data["Date"])
data["Year"] = data["Date"].dt.year
data = data[["Year", "Magnitude"]]

# Train model
X = data.drop("Magnitude", axis=1)
y = data["Magnitude"]
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

# Generate predictions for every year from 2021 to 2029
years = range(2021, 2024)
predictions = []
for year in years:
    prediction = model.predict([[year]])
    predictions.append(prediction[0])

# Calculate probability of earthquakes above 7.5 magnitude for each year from 2021 to 2029
threshold = 7.5
probabilities = 1 - (1 / (1 + np.exp(np.array(predictions) - threshold)))

# Print results
for i, year in enumerate(years):
    print(f"{year}: {probabilities[i]:.2%}")


# In[328]:


import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

data = pd.read_csv("turkey_earthquakes(1915-2021).csv", delimiter=";")
del data["No"]
data = data.rename(
    columns={
        "Deprem Kodu": "Code",
        "Olus tarihi": "Date",
        "Olus zamani": "Time",
        "Enlem": "Latitude",
        "Boylam": "Longitude",
        "Derinlik": "Depth",
        "xM": "Magnitude",
        "Yer": "Location",
    },
)
del data["Code"], data["Tip"], data["MD"], data["ML"], data["Mw"], data["Ms"], data["Mb"]
data = data.iloc[::-1].reset_index(drop=True)

# Preprocess data
data["Date"] = pd.to_datetime(data["Date"])
data["Year"] = data["Date"].dt.year
data["Month"] = data["Date"].dt.month
data = data[["Year", "Month", "Magnitude"]]

# Split data into training and test sets
train = data[data["Year"] <= 1980]
test = data[data["Year"] >= 1980]

# Train model
X_train = train.drop("Magnitude", axis=1)
y_train = train["Magnitude"]
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Generate predictions for test set
X_test = test.drop("Magnitude", axis=1)
y_test = test["Magnitude"]
predictions = model.predict(X_test)

# Calculate mean absolute error (MAE)
mae = mean_absolute_error(y_test, predictions)
print(f"MAE: {mae:.2f}")

# Generate predictions for every month in 2023
months = pd.date_range(start="2022-01-01", end="2022-12-31", freq="M")
predictions = []
for month in months:
    year = month.year
    month = month.month
    prediction = model.predict([[year, month]])
    predictions.append(prediction[0])

# Calculate probability of earthquakes above 7.8 magnitude for each month in 2023
threshold = 7.8
probabilities = 1 - (1 / (1 + np.exp(np.array(predictions) - threshold)))

# Print results
for i, month in enumerate(months):
    print(f"{month}: {probabilities[i]:.2%}")

print(f"MAE: {mae:.2f}")


# In[320]:


df.info()


# In[341]:


before=pd.read_csv("before.csv")
after=pd.read_csv("after.csv")
before = before.iloc[2:]
len(before)


# In[345]:


from scipy import stats

# H0: Price before > after   ha: Price before< after
stats.ttest_rel(before,after,alternative="less")


# In[346]:


pop_b=[1.483894253,1.398832876,1.322750764,1.363157579,1.347579064,1.296589085,1.238731837,1.201593459,1.260812125,1.333673238]
pop_a=[1.327989006,1.476875893,1.710476458,1.985938915,1.944942151,1.709450784,1.312552862,0.87263355,0.808683227,0.780048418]

# H0: Price before > after   ha: Price before< after
stats.ttest_rel(pop_b,pop_a,alternative="less")


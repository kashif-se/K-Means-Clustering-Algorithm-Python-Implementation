
# coding: utf-8

# <p style="font-family: Arial; font-size:2.75em;color:purple; font-style:bold"><br>
# 
# Clustering with scikit-learn
# 
# <br><br></p>

# In this notebook, we will learn how to perform k-means lustering using scikit-learn in Python. 
# 
# We will use cluster analysis to generate a big picture model of the weather at a local station using a minute-graunlarity data. In this dataset, we have in the order of millions records. How do we create 12 clusters our of them?
# 
# **NOTE:** The dataset we will use is in a large CSV file called *minute_weather.csv*. Please download it into the *weather* directory in your *Week-7-MachineLearning* folder. The download link is: https://drive.google.com/open?id=0B8iiZ7pSaSFZb3ItQ1l4LWRMTjg 

# <p style="font-family: Arial; font-size:1.75em;color:purple; font-style:bold"><br>
# 
# Importing the Necessary Libraries<br></p>

# In[2]:

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
#import utils
import pandas as pd
import numpy as np
from itertools import cycle, islice
import matplotlib.pyplot as plt
from pandas.plotting import parallel_coordinates

#get_ipython().magic('matplotlib inline')


# <p style="font-family: Arial; font-size:1.75em;color:purple; font-style:bold"><br>
# 
# Creating a Pandas DataFrame from a CSV file<br><br></p>
# 

# In[3]:

data = pd.read_csv('E:\\ITU\\Semester 2\\Big Data Analytics\\Assignments\\Assignment 1\\daily_weather.csv')


# <p style="font-family: Arial; font-size:1.75em;color:purple; font-style:bold">Minute Weather Data Description</p>
# <br>
# The **minute weather dataset** comes from the same source as the daily weather dataset that we used in the decision tree based classifier notebook. The main difference between these two datasets is that the minute weather dataset contains raw sensor measurements captured at one-minute intervals. Daily weather dataset instead contained processed and well curated data. The data is in the file **minute_weather.csv**, which is a comma-separated file.
# 
# As with the daily weather data, this data comes from a weather station located in San Diego, California. The weather station is equipped with sensors that capture weather-related measurements such as air temperature, air pressure, and relative humidity. Data was collected for a period of three years, from September 2011 to September 2014, to ensure that sufficient data for different seasons and weather conditions is captured.
# 
# Each row in **minute_weather.csv** contains weather data captured for a one-minute interval. Each row, or sample, consists of the following variables:
# 
# * **rowID:** 	unique number for each row	(*Unit: NA*)
# * **hpwren_timestamp:**	timestamp of measure	(*Unit: year-month-day hour:minute:second*)
# * **air_pressure:** air pressure measured at the timestamp	(*Unit: hectopascals*)
# * **air_temp:**	air temperature measure at the timestamp	(*Unit: degrees Fahrenheit*)
# * **avg_wind_direction:**	wind direction averaged over the minute before the timestamp	(*Unit: degrees, with 0 means coming from the North, and increasing clockwise*)
# * **avg_wind_speed:**	wind speed averaged over the minute before the timestamp	(*Unit: meters per second*)
# * **max_wind_direction:**	highest wind direction in the minute before the timestamp	(*Unit: degrees, with 0 being North and increasing clockwise*)
# * **max_wind_speed:**	highest wind speed in the minute before the timestamp	(*Unit: meters per second*)
# * **min_wind_direction:**	smallest wind direction in the minute before the timestamp	(*Unit: degrees, with 0 being North and inceasing clockwise*)
# * **min_wind_speed:**	smallest wind speed in the minute before the timestamp	(*Unit: meters per second*)
# * **rain_accumulation:**	amount of accumulated rain measured at the timestamp	(*Unit: millimeters*)
# * **rain_duration:**	length of time rain has fallen as measured at the timestamp	(*Unit: seconds*)
# * **relative_humidity:**	relative humidity measured at the timestamp	(*Unit: percent*)

# In[4]:

data.shape


# In[5]:

data.head()


# <p style="font-family: Arial; font-size:1.75em;color:purple; font-style:bold"><br>
# 
# Data Sampling<br></p>
# 
# Lots of rows, so let us sample down by taking every 10th row. <br>
# 

# In[8]:

sampled_df = data[:]
sampled_df.shape


# <p style="font-family: Arial; font-size:1.75em;color:purple; font-style:bold"><br>
# 
# Statistics
# <br><br></p>
# 

# In[9]:

sampled_df.describe().transpose()


# In[11]:

sampled_df[sampled_df['rain_accumulation_9am'] == 0].shape


# In[12]:

sampled_df[sampled_df['rain_duration_9am'] == 0].shape


# <p style="font-family: Arial; font-size:1.75em;color:purple; font-style:bold"><br>
# 
# Drop all the Rows with Empty rain_duration and rain_accumulation
# <br><br></p>
# 

# In[15]:

#del sampled_df['rain_accumulation_9am']
del sampled_df['rain_duration_9am']


# In[16]:

rows_before = sampled_df.shape[0]
sampled_df = sampled_df.dropna()
rows_after = sampled_df.shape[0]


# <p style="font-family: Arial; font-size:1.75em;color:purple; font-style:bold"><br>
# 
# How many rows did we drop ?
# <br><br></p>
# 

# In[17]:

rows_before - rows_after


# In[18]:

sampled_df.columns


# <p style="font-family: Arial; font-size:1.75em;color:purple; font-style:bold"><br>
# 
# Select Features of Interest for Clustering
# <br><br></p>
# 

# In[22]:

features = ['air_pressure_9am', 'air_temp_9am', 'avg_wind_direction_9am', 'avg_wind_speed_9am', 'max_wind_direction_9am', 
        'max_wind_speed_9am','relative_humidity_9am']


# In[23]:

select_df = sampled_df[features]


# In[24]:

select_df.columns


# In[25]:

select_df


# <p style="font-family: Arial; font-size:1.75em;color:purple; font-style:bold"><br>
# 
# Scale the Features using StandardScaler
# <br><br></p>
# 

# In[26]:

X = StandardScaler().fit_transform(select_df)
X


# <p style="font-family: Arial; font-size:1.75em;color:purple; font-style:bold"><br>
# 
# Use k-Means Clustering
# <br><br></p>
# 

# In[27]:

kmeans = KMeans(n_clusters=12)
model = kmeans.fit(X)
print("model\n", model)


# <p style="font-family: Arial; font-size:1.75em;color:purple; font-style:bold"><br>
# 
# What are the centers of 12 clusters we formed ?
# <br><br></p>
# 

# In[29]:

centers = model.cluster_centers_
centers.shape


# <p style="font-family: Arial; font-size:2.75em;color:purple; font-style:bold"><br>
# 
# Plots
# <br><br></p>
# 

# Let us first create some utility functions which will help us in plotting graphs:

# In[30]:

# Function that creates a DataFrame with a column for Cluster Number

def pd_centers(featuresUsed, centers):
	colNames = list(featuresUsed)
	colNames.append('prediction')

	# Zip with a column called 'prediction' (index)
	Z = [np.append(A, index) for index, A in enumerate(centers)]

	# Convert to pandas data frame for plotting
	P = pd.DataFrame(Z, columns=colNames)
	P['prediction'] = P['prediction'].astype(int)
	return P


# In[31]:

# Function that creates Parallel Plots

def parallel_plot(data):
	my_colors = list(islice(cycle(['b', 'r', 'g', 'y', 'k']), None, len(data)))
	plt.figure(figsize=(15,8)).gca().axes.set_ylim([-3,+3])
	parallel_coordinates(data, 'prediction', color = my_colors, marker='o')


# In[32]:

P = pd_centers(features, centers)
P


# # Dry Days

# In[34]:

parallel_plot(P[P['relative_humidity_9am'] < -0.5])


# # Warm Days

# In[36]:

parallel_plot(P[P['air_temp_9am'] > 0.5])


# # Cool Days

# In[39]:

parallel_plot(P[(P['relative_humidity_9am'] > 0.5) & (P['air_temp_9am'] < 0.5)])


# In[ ]:




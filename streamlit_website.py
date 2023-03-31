import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import requests
import pylab

import numpy as np
from scipy.stats import *
import seaborn as sns
import statsmodels.api as sm
from sklearn.model_selection import train_test_split
from bokeh.plotting import figure
x1 = []
y1 = []
sns.set()
import plotly.graph_objects as go
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
emission = pd.read_csv("greenhouse.csv")
emission.rename({"country_or_area": "country"}, axis=1, inplace=True)
emission["text"] = "Location: " + emission["country"]
unique = emission.country.unique()

emission["country"] = le.fit_transform(emission["country"])
from sklearn import svm
X = emission.drop(["country", "category", "year", "text"], axis=1) # X = emission.value
y = emission["country"].values.reshape(-1,1)
X_train, X_test, Y_train, Y_test = train_test_split(X, y, test_size=0.2)
model = svm.SVC(C=0.02, gamma=0.06)
model.fit(X_train, Y_train)
pred = model.predict(X_test)







fig = go.Figure(data=go.Choropleth(
    locations=emission["text"],
    z=emission["value"].astype(float),
    locationmode="country names",
    colorscale="thermal",
    colorbar_title="emission",
    text=emission["text"] # Hover text
))

fig.update_layout(
    title_text="Greenhouse emission",
    geo_scope="world",
    
)


for i in range(-10, 11):
    x1.append(i)
    y1.append(i**2)
df = pd.DataFrame({
    "x": x1,
    "y": y1
})
current = requests.get("http://api.weatherapi.com/v1/current.json?key=4a1f9e155ac6494e98a15506222712&q=London&aqi=yes") 
forecast = requests.get("http://api.weatherapi.com/v1/forecast.json?key=4a1f9e155ac6494e98a15506222712&q=SE93HX&days=5&aqi=yes&alerts=yes")

print ("code: {}".format(current.status_code))



#df = response_hourly.text


print ("\n")
print (current.text)

file = open("3_hour_forecast.json", "w")
file.write(current.text)
file.close()
f1 = pd.read_json("3_hour_forecast.json", "r")

import json
import csv
import pandas as pd


import json
import csv
 
with open('3_hour_forecast.json') as json_file:
    jsondata = json.load(json_file)
 
data_file = open('weather_forecast.csv', 'w', newline='')
csv_writer = csv.writer(data_file)
 
count = 0
for data in jsondata:
    if count == 0:
        header = jsondata[data].keys()
        csv_writer.writerow(header)
        count += 1
    csv_writer.writerow(jsondata[data].values())
 
data_file.close()

temp_df = pd.read_csv("weather_forecast.csv", delimiter=';', skiprows=0, low_memory=False)
temp_df = temp_df.fillna("0")




st.set_page_config(page_title="Weather Data", page_icon=":tada:", layout="wide")
with st.container():
    st.write("---")
    left_column, right_column = st.columns(2)
    with left_column:
        st.header("What I do")
        st.write("""""
                 
                 I am a 2nd year Biomediicne student.
                 
                 I also like coding
                 :)
                 
                 
                 
                 
                 
                 """)
    with right_column:
        st.header("My projects:")
        st.write("Weather Prediction data :)")
        st.write("Money prediction A.I")
with st.container():
    st.subheader("Hi, I am Thomas :wave:")
    st.title("HELLO, FATHER")
    st.write("This website will contain my weather prediction data")

json_df = pd.read_json("3_hour_forecast.json")
json_df = json_df.fillna("0")

# This section will provide a forecast table

json_df = pd.read_json("3_hour_forecast.json")
json_df = json_df.fillna("0")


forecast_file = open("forecast.json", "w")
forecast_file.write(forecast.text)
forecast_file.close()

forecast_df = pd.read_json("forecast.json")
forecast_df = forecast_df.fillna("0")

weather_forecast = forecast_df["forecast"]["forecastday"]
weather_forecast = pd.DataFrame(weather_forecast)

with st.container():
    left_column, right_column = st.columns(2)
    
    with left_column:
        st.title("Current Data for Eltham, UK")
        st.dataframe(json_df)
    with right_column:
        st.title("Forecast Data for Eltham, UK")
        st.dataframe(forecast_df)

with st.container():
    st.title("Forecast data for Eltham, London, UK")
    st.dataframe(weather_forecast, use_container_width=True)
    ##########################################################
    #########################################################
    
    astro = weather_forecast.astro 
    
    
with st.container():
    st.plotly_chart(fig, use_container_width=True)
        
with st.container():
    st.title("Prototype slider estimate")
    st.write("The accuracy for this model is: ".format(model.score(Y_test, pred) * 100))
    st.write(model.score(Y_test, pred) * 100)
    
    new_input = st.slider(
        "Slide for an Estimate", 0, 7422208, 1000
    )
    new_input = int(new_input)
    new_input = np.array(new_input)
    new_input = np.reshape(new_input, (-1, 1))
    st.write(f"Prediction ID: {model.predict(new_input)}")
    st.write(f"Country Prediction: {unique[model.predict(new_input)]}")
with st.container():
    option = st.selectbox(
        "Which Country would You like to visualize?",
        unique,
        
    ) 
    st.write("Current Option: " + option)
selection = emission[emission.country == f"{option}"]
selection = selection.groupby(["year"])["value"].mean()
new = pd.DataFrame(selection)
new["year"] = [i for i in new.index]
fig1, o = plt.subplots()
fig1.suptitle("title")
o.plot(new.year, new.value)
o.set_xlabel("Year")
o.set_ylabel("value")
o.set_title("Mean Greenhouse emission for " + option)

with st.container():
    st.pyplot(fig1, clear_figure=False)
    
        
        
        
# I can add a checkbox to visualise graphs for greenhosue emission for each country
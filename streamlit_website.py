import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import requests

x1 = []
y1 = []

for i in range(-10, 11):
    x1.append(i)
    y1.append(i**2)
df = pd.DataFrame({
    "x": x1,
    "y": y1
})
locationID_hourly = requests.get("http://api.weatherapi.com/v1/current.json?key=4a1f9e155ac6494e98a15506222712&q=SE93HX&aqi=no") 
forecast = requests.get("http://api.weatherapi.com/v1/forecast.json?key=4a1f9e155ac6494e98a15506222712&q=SE93HX&days=1&aqi=yes&alerts=yes")

print ("code: {}".format(locationID_hourly.status_code))



#df = response_hourly.text


print ("\n")
print (locationID_hourly.text)

file = open("3_hour_forecast.json", "w")
file.write(locationID_hourly.text)
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


with st.container():
    left_column, right_column = st.columns(2)
    
    with left_column:
        st.title("Current Data for Eltham, UK")
        st.dataframe(json_df)
    with right_column:
        st.title("Forecast Data for Eltham, UK")
        st.dataframe(forecast_df)
        
    
    
    
    
    
    

        
        
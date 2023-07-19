import streamlit as st

import pandas as pd

import requests


import numpy as np
from scipy.stats import *



from bokeh.plotting import figure
sns.set()
import plotly.graph_objects as go

import itertools
from bokeh.palettes import inferno

from test_AI import *
le = LabelEncoder()


unique = emission.country.unique()


from world_emission_plot import *




current = requests.get("http://api.weatherapi.com/v1/current.json?key=4a1f9e155ac6494e98a15506222712&q=London&aqi=yes") 
forecast = requests.get("http://api.weatherapi.com/v1/forecast.json?key=4a1f9e155ac6494e98a15506222712&q=SE93HX&days=5&aqi=yes&alerts=yes")

print ("code: {}".format(current.status_code))






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
   
   
## A.I section     


## Design a multi-selector
with st.container():
    
    st.title("Prototype slider estimate")
    st.write("The accuracy for this model is:")
    st.write(accuracy)
    
    
    ## This part is the model inputs
    ## The left column contains year and value
    ## Right column contains category and language
    
    ## A button will be included to confirm input
    
    left_column, right_column = st.columns(2)
    
    with left_column:
        
        value_input = st.slider(
        "Value", 0, 7422208, 1000
        )
        
        year_input = st.slider(
            "year", 1990, 2014, 2000
        )
        
        
    
    with right_column:
        ## Here, I need to match the string value to the encoded value
        
        unique_categories = emission.category.unique()
        unique_languages = emission.official_language.unique()
        
        category_input = st.selectbox(
            "Select the emission category",
            unique_categories
        )
        
        category_input = emission[emission.category == category_input]["category_encoded"].unique()
        
        
        
        
        
        language_input = st.selectbox(
            "select the official language",
            unique_languages
        )
        
        
        language_input = emission[emission.official_language == language_input]["official_language_encoded"].unique()
        
        
    
        
        
    ## MODEL INPUT
    ## I place all inputs into a dataframe
    
    input_values = np.array([year_input, value_input, category_input, language_input])
    
    input_values = np.reshape(input_values, (1,4))
    
    input_values = pd.DataFrame(input_values, columns=["year", "value", "category_encoded", "official_language_encoded"])
    
    
    ID = model.predict(input_values)
    
    
    st.write(f"Prediction ID: {ID}") 
    
    ID = int(ID)
    prediction = unique[ID]
    st.write("Country Prediction: " + prediction)
     
    
    
with st.container():
    option = st.selectbox(
        "Which Country would You like to visualize?",
        unique,
        
    ) 
    st.write("Current Option: " + option)

hopefully_works = pd.read_csv("greenhouse.csv")
selection = hopefully_works[hopefully_works.country== option]


## Plotting average emissions per year for a selected country
new = selection.groupby(["year"])["value"].mean()

new["year"] = [i for i in new.index]

st.dataframe(new)
new1 = pd.DataFrame(new)
new1["Year"] = [i for i in new1.index] 

st.write("Mean greenhouse emission per year for " + option)
from bokeh.plotting import figure


p = figure(
    title='greenhouse emission for ' + option,
    x_axis_label='year',
    y_axis_label='value')

p.line(new1.Year, new1.value, legend_label='Trend', line_width=2)



st.bokeh_chart(p, use_container_width=True)

# hopefully_works



new_df = hopefully_works[hopefully_works.country == option]
new_df = new_df.pivot_table(columns="category", index="year", values="value")
with st.container():
    a = figure(
        title = ("Greenhouse emission categories for " + option),
        x_axis_label = "year",
        y_axis_label = "value"
    )
    colors = itertools.cycle(inferno(len(new_df.columns)))
    for i in new_df.columns:
        a.line(x=new_df.index, y=new_df[i], legend_label=i, color=next(colors))
        
    st.bokeh_chart(a, use_container_width=True)
        
## Next, I will add a more advanced plot
## Which will show mean greenhouse emissions in a country for each category
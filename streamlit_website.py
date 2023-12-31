import streamlit as st
import pandas as pd
import requests
import numpy as np
from scipy.stats import *
from bokeh.plotting import figure

import plotly.graph_objects as go
from sklearn.preprocessing import LabelEncoder
import itertools
from bokeh.palettes import inferno
from test_AI import *
le = LabelEncoder()
unique = emission.country.unique()
from world_emission_plot import *
import shap


current = requests.get("http://api.weatherapi.com/v1/current.json?key=4a1f9e155ac6494e98a15506222712&q=London&aqi=yes")
forecast = requests.get("http://api.weatherapi.com/v1/forecast.json?key=4a1f9e155ac6494e98a15506222712&q=SE93HX&days=5&aqi=yes&alerts=yes")

print ("code: {}".format(current.status_code))






print ("\n")
print (current.text)

import json
import csv
import pandas as pd

json_df = pd.read_json(current.text)
forecast_df = pd.read_json(forecast.text)
json_df.fillna("0", inplace=True)
forecast_df.fillna('0', inplace=True)

st.set_page_config(page_title="Weather Data", page_icon=":tada:", layout="wide")
with st.container():
    st.subheader("Hi, I am Thomas :wave:")
    st.write("This website will contain my weather prediction data")



with st.container():
    st.write("---")
    left_column, right_column = st.columns(2)
    with left_column:
        st.header("Part 1")
        st.write("""

                 This project means to predict the weather by:
                 
                 1. Collecting historical weather data
                 2. Building an ML model to predict weather conditions
                 
                 
                 


                 """)
    with right_column:
        st.header("Part 2")
        st.write("""
                 A secondary goal of  this project is to present global emission data through geo-spacial plots
                 Upon this, I will perform time series analysis to detect anomalies
                 
                 """)
        

# This section will provide a forecast table






weather_forecast = forecast_df["forecast"]["forecastday"]

## reshaping the forecast data
forecast_df = pd.DataFrame(weather_forecast)
forecast_values = forecast_df.values

transposed_forecast_df = pd.DataFrame(forecast_values.T)
transposed_forecast_df.columns = transposed_forecast_df.iloc[0]

transposed_forecast_df.drop(index=0, axis=0, inplace=True)
transposed_forecast_df.drop(index=1, axis=0, inplace=True)
transposed_forecast_df.reset_index(inplace=True)


transposed_forecast_df.drop(["index"], axis=1,inplace=True)
new_index1 = [i for i in transposed_forecast_df[transposed_forecast_df.columns[0]].iloc[0]]
new_index2 = [i for i in transposed_forecast_df[transposed_forecast_df.columns[1]].iloc[1]]
new_index3 = [i for i in transposed_forecast_df[transposed_forecast_df.columns[2]].iloc[2][0].keys()]

indexes = [*new_index1, *new_index2, *new_index3]

columns = transposed_forecast_df.columns

## Creating a new dataframe
forecast_df = pd.DataFrame()
forecast_df[transposed_forecast_df.columns[0]] = [*transposed_forecast_df[transposed_forecast_df.columns[0]].iloc[0].values(), *transposed_forecast_df[transposed_forecast_df.columns[0]].iloc[1].values(), *dict(transposed_forecast_df[transposed_forecast_df.columns[0]].iloc[2][0]).values()]
forecast_df[transposed_forecast_df.columns[1]] = [*transposed_forecast_df[transposed_forecast_df.columns[1]].iloc[0].values(), *transposed_forecast_df[transposed_forecast_df.columns[1]].iloc[1].values(), *dict(transposed_forecast_df[transposed_forecast_df.columns[1]].iloc[2][0]).values()]
forecast_df[transposed_forecast_df.columns[2]] = [*transposed_forecast_df[transposed_forecast_df.columns[2]].iloc[0].values(), *transposed_forecast_df[transposed_forecast_df.columns[2]].iloc[1].values(), *dict(transposed_forecast_df[transposed_forecast_df.columns[2]].iloc[2][0]).values()]
forecast_df.index = indexes



## I should create separate dataframes for each day in weather_forecast



with st.container():
    st.title("Current Data for Eltham, UK")
    st.dataframe(json_df, use_container_width=True)
    


with st.container():
    st.title("Forecast Data For Eltham, UK")
    st.dataframe(forecast_df, use_container_width=True)
    
    
with st.container():
    st.plotly_chart(fig, use_container_width=True)


## A.I section


## Design a multi-selector
st.title("Greenhouse Classification Model and Explanation")
model_tab, explanation_tab = st.tabs(["model", "explanation"])
with model_tab:

    st.header("Greenhouse Classification Model")
    st.write(f"test accuracy: {accuracy}")
    st.write(f"training accuracy: {train_accuracy}")
    st.write(f"f1 score: {f1}")
    st.write(f"recall: {recall}")
    st.write(f"precision: {precision}")



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

        #category_input = emission[emission.category == category_input]["category"].unique()





        language_input = st.selectbox(
            "select the official language",
            unique_languages
        )


        #language_input = emission[emission.official_language == language_input]["official_language"].unique()






    ## I place all inputs into a dataframe

    ## Unique encoded countries
    unique_encoded_countries = new_emission.country.unique()

    ## Unique encoded categories
    unique_encoded_categories = new_emission.category.unique()

    ## Unique official language
    unique_encoded_languages = new_emission.official_language.unique()


    ## Matching encoded values to string types

    ## Indexes should be the same

    countries = [i for i in zip(unique, unique_encoded_countries)]
    categories = [i for i in zip(unique_categories, unique_encoded_categories)]
    languages = [i for i in zip(unique_languages, unique_encoded_languages)]


    ## Matching the inputted country, category and langauges to their encoded types

    ## I need to find where the input matches the [0] index of categories and languages

    st.write("\n \n \n \n")
    input_category = []
    input_language = []
    for i in range(len(categories)):
        if categories[i][0] == category_input:
            input_category.append(categories[i][1])
        else:
            pass

    for i in range(len(languages)):
        if languages[i][0] == language_input:
            input_language.append(languages[i][1])
        else:
            pass

    ### MODEL Input

    input_values = np.array([year_input, value_input, input_category[0], input_language[0]])

    input_values = np.reshape(input_values, (1,4))

    input_values = pd.DataFrame(input_values, columns=["year", "value", "category", "official_language"])


    ID = model.predict(input_values)


    st.write(f"Prediction ID: {ID}")

    ID = int(ID)
    prediction = unique[ID]
    st.write("Country Prediction: " + prediction)

with explanation_tab:
    #explainer = shap.TreeExplainer(model, X_test, feature_names=X_test.columns)
    #shap_values = explainer(input_values)
    
    
    ## Displaying the SHAP explanation
    ## error returns 
    #st_shap(shap.initjs())
    #st_shap(shap.force_plot(explainer.expected_value[0], shap_values.values[0], feature_names=X_test.columns))
    st.write("under development...")


#####################
st.write("\n \n \n")
with st.container():
    st.title("Greenhouse emission Analysis")
    option = st.selectbox(
            "Which Country would You like to visualize?",
            unique,

        )
    st.write("Current Option: " + option)
    hopefully_works = pd.read_csv("greenhouse.csv")
    selection = hopefully_works[hopefully_works.country== option]



## Forming tabs
mean_country_tab, emission_tab = st.tabs(["Mean Emissions", "Each Emission"])



with mean_country_tab:



    ## Plotting average emissions per year for a selected country
    new = selection.groupby(["year"])["value"].mean()

    new["year"] = [i for i in new.index]


    new1 = pd.DataFrame(new)
    new1["Year"] = [i for i in new1.index]

    st.write("Mean greenhouse emission per year for " + option)
    from bokeh.plotting import figure, show


    p = figure(
        title='greenhouse emission for ' + option,
        x_axis_label='year',
        y_axis_label='value')

    p.line(new1.Year, new1.value, legend_label='Trend', line_width=2)
    st.bokeh_chart(p, use_container_width=True)

# hopefully_works

with emission_tab:
    new_df = hopefully_works[hopefully_works.country == option]
    new_df = new_df.pivot_table(columns="category", index="year", values="value")

    a = figure(
        title = ("Greenhouse emission categories for " + option),
        x_axis_label = "year",
        y_axis_label = "value"
    )
    colors = itertools.cycle(inferno(len(new_df.columns)))
    for i in new_df.columns:
        a.line(x=new_df.index, y=new_df[i], legend_label=i, color=next(colors))

    st.bokeh_chart(a, use_container_width=True)

## I can also do some time series analysis here

#========================================
### What should this networkx graph show?
## I can add a networkx plot (using tabs) detailing how
## Emissions vary with countries and regions
## The connecting factor can be the types of emissions
##


#========================================
## I can also use the historical dataset


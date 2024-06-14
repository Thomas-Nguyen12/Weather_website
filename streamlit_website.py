import streamlit as st
import pandas as pd
import requests
import numpy as np
import shap
from streamlit_shap import st_shap
from sklearn.preprocessing import LabelEncoder
import itertools
from bokeh.palettes import inferno
from bokeh.plotting import figure
import matplotlib.pyplot as plt 
import shap.explainers._tree
import joblib
import pickle
import lime 
from lime import lime_tabular
# Custom unpickler to handle missing attributes
model = joblib.load("weather_model.pkl")
explainer = joblib.load("explainer.pkl")
shap_values = joblib.load("weather_shap_values.pkl")
train_accuracy = joblib.load("train_accuracy.pkl")
accuracy = joblib.load("accuracy.pkl")
f1 = joblib.load("f1.pkl")
precision = joblib.load("precision.pkl")
recall = joblib.load("recall.pkl")
emission = joblib.load("emission.pkl")


# Additional setup
le = LabelEncoder()
unique = emission.country.unique()

# Fetch current weather and forecast data
current = requests.get("http://api.weatherapi.com/v1/current.json?key=4a1f9e155ac6494e98a15506222712&q=London&aqi=yes")
forecast = requests.get("http://api.weatherapi.com/v1/forecast.json?key=4a1f9e155ac6494e98a15506222712&q=SE93HX&days=5&aqi=yes&alerts=yes")

# Process weather data
json_df = pd.read_json(current.text)
forecast_df = pd.read_json(forecast.text)
json_df.fillna("0", inplace=True)
forecast_df.fillna('0', inplace=True)

# Transpose forecast data for better display
weather_forecast = forecast_df["forecast"]["forecastday"]
forecast_df = pd.DataFrame(weather_forecast)
forecast_values = forecast_df.values

transposed_forecast_df = pd.DataFrame(forecast_values.T)
transposed_forecast_df.columns = transposed_forecast_df.iloc[0]

transposed_forecast_df.drop(index=[0, 1], axis=0, inplace=True)
transposed_forecast_df.reset_index(inplace=True, drop=True)

new_index1 = [i for i in transposed_forecast_df[transposed_forecast_df.columns[0]].iloc[0]]
new_index2 = [i for i in transposed_forecast_df[transposed_forecast_df.columns[1]].iloc[1]]
new_index3 = [i for i in transposed_forecast_df[transposed_forecast_df.columns[2]].iloc[2][0].keys()]

indexes = [*new_index1, *new_index2, *new_index3]
forecast_df = pd.DataFrame({
    transposed_forecast_df.columns[0]: [*transposed_forecast_df[transposed_forecast_df.columns[0]].iloc[0].values(), 
                                        *transposed_forecast_df[transposed_forecast_df.columns[0]].iloc[1].values(), 
                                        *dict(transposed_forecast_df[transposed_forecast_df.columns[0]].iloc[2][0]).values()],
    transposed_forecast_df.columns[1]: [*transposed_forecast_df[transposed_forecast_df.columns[1]].iloc[0].values(), 
                                        *transposed_forecast_df[transposed_forecast_df.columns[1]].iloc[1].values(), 
                                        *dict(transposed_forecast_df[transposed_forecast_df.columns[1]].iloc[2][0]).values()],
    transposed_forecast_df.columns[2]: [*transposed_forecast_df[transposed_forecast_df.columns[2]].iloc[0].values(), 
                                        *transposed_forecast_df[transposed_forecast_df.columns[2]].iloc[1].values(), 
                                        *dict(transposed_forecast_df[transposed_forecast_df.columns[2]].iloc[2][0]).values()]
})
forecast_df.index = indexes

# Set up Streamlit app
st.set_page_config(page_title="Weather Data", page_icon=":tada:", layout="wide")

# Header
with st.container():
    st.subheader("Hi, I am Thomas :wave:")
    st.write("This website will contain my weather prediction data")

# Project Description
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
                 A secondary goal of this project is to present global emission data through geo-spatial plots.
                 Upon this, I will perform time series analysis to detect anomalies.
                 """)

# Current Weather Data
with st.container():
    st.title("Current Data for Eltham, UK")
    st.dataframe(json_df, use_container_width=True)

# Forecast Data
with st.container():
    st.title("Forecast Data For Eltham, UK")
    st.dataframe(forecast_df, use_container_width=True)

# Greenhouse Classification Model
st.title("Greenhouse Classification Model and Explanation")
model_tab, explanation_tab = st.tabs(["Model", "Explanation"])
with model_tab:
    st.header("Greenhouse Classification Model")
    st.write(f"Test Accuracy: {accuracy}")
    st.write(f"Training Accuracy: {train_accuracy}")
    st.write(f"F1 Score: {f1}")
    st.write(f"Recall: {recall}")
    st.write(f"Precision: {precision}")

    left_column, right_column = st.columns(2)
    with left_column:
        value_input = st.slider("Value", 0, 7422208, 1000)
        year_input = st.slider("Year", 1990, 2014, 2000)
    with right_column:
        unique_categories = emission.category.unique()
        unique_languages = emission.official_language.unique()
        category_input = st.selectbox("Select the emission category", unique_categories)
        language_input = st.selectbox("Select the official language", unique_languages)

    # Encoding input values
    categories = {val: idx for idx, val in enumerate(unique_categories)}
    languages = {val: idx for idx, val in enumerate(unique_languages)}

    input_category = categories[category_input]
    input_language = languages[language_input]

    input_values = np.array([year_input, value_input, input_category, input_language]).reshape(1, -1)
    prediction = model.predict(input_values)
    country_prediction = unique[int(prediction[0])]

    st.write(f"Prediction ID: {prediction[0]}")
    st.write(f"Country Prediction: {country_prediction}")

with explanation_tab:
    st.header("Model Explanation with SHAP")
    st_shap(shap.initjs())
    

    
    st_shap(shap.summary_plot(shap_values[:, :, 0]))
    #st_shap(shap.force_plot(shap_values[:, :, 0]))


    #shap.force_plot(explainer.expected_value, shap_values[0])

# Greenhouse Emission Analysis
st.write("\n \n \n")
with st.container():
    st.title("Greenhouse Emission Analysis")
    option = st.selectbox("Which Country would You like to visualize?", unique)
    st.write("Current Option: " + option)
    hopefully_works = pd.read_csv("greenhouse.csv")
    selection = hopefully_works[hopefully_works.country == option]

mean_country_tab, emission_tab = st.tabs(["Mean Emissions", "Each Emission"])

with mean_country_tab:
    new = selection.groupby(["year"])["value"].mean().reset_index()
    p = figure(title=f'Greenhouse Emission for {option}', x_axis_label='year', y_axis_label='value')
    p.line(new["year"], new["value"], legend_label='Trend', line_width=2)
    st.bokeh_chart(p, use_container_width=True)

with emission_tab:
    new_df = selection.pivot_table(columns="category", index="year", values="value")
    a = figure(title=f'Greenhouse Emission Categories for {option}', x_axis_label='year', y_axis_label='value')
    colors = itertools.cycle(inferno(len(new_df.columns)))
    for col in new_df.columns:
        a.line(new_df.index, new_df[col], legend_label=col, color=next(colors))
    st.bokeh_chart(a, use_container_width=True)

# Further analysis can be added here
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
import os

from dotenv import load_dotenv
load_dotenv()

# --- Load model and data ---
model = joblib.load("models/weather_model.pkl")
X_test = joblib.load("data/X_test.pkl")
shap_values = joblib.load("metrics/weather_shap_values.pkl")
train_accuracy = joblib.load("metrics/train_accuracy.pkl")
accuracy = joblib.load("metrics/accuracy.pkl")
f1 = joblib.load("metrics/f1.pkl")
precision = joblib.load("metrics/precision.pkl")
recall = joblib.load("metrics/recall.pkl")
emission = joblib.load("data/emission.pkl")

unique = emission.country.unique()

current_api_key = os.environ.get("current_api_key")
forecast_api_key = os.environ.get("forecast_api_key")

# --- Fetch current weather data with error handling ---
try:
    current = requests.get(
        f"http://api.weatherapi.com/v1/current.json?key={current_api_key}&q=London&aqi=yes",
        timeout=10
    )
    current.raise_for_status()
    json_df = pd.read_json(current.text, encoding='utf-8-sig')
    json_df.fillna("0", inplace=True)
except Exception as e:
    st.error(f"Failed to fetch current weather data: {e}")
    json_df = pd.DataFrame()

# --- Fetch forecast data with error handling ---
try:
    forecast = requests.get(
        f"http://api.weatherapi.com/v1/forecast.json?key={forecast_api_key}&q=New Eltham&days=5&aqi=yes&alerts=yes",
        timeout=10
    )
    forecast.raise_for_status()
    forecast_raw = pd.read_json(forecast.text, encoding='utf-8-sig')
    forecast_raw.fillna('0', inplace=True)

    weather_forecast = forecast_raw["forecast"]["forecastday"]
    forecast_df = pd.DataFrame(weather_forecast)
    forecast_values = forecast_df.values

    transposed_forecast_df = pd.DataFrame(forecast_values.T)
    transposed_forecast_df.columns = transposed_forecast_df.iloc[0]
    transposed_forecast_df.drop(index=[0, 1], axis=0, inplace=True)
    transposed_forecast_df.reset_index(inplace=True, drop=True)

    col0 = transposed_forecast_df.columns[0]
    col1 = transposed_forecast_df.columns[1]
    col2 = transposed_forecast_df.columns[2]

    new_index1 = list(transposed_forecast_df[col0].iloc[0].keys())
    new_index2 = list(transposed_forecast_df[col1].iloc[1].keys())
    new_index3 = list(transposed_forecast_df[col2].iloc[2][0].keys())
    indexes = [*new_index1, *new_index2, *new_index3]

    forecast_df = pd.DataFrame({
        col0: [
            *transposed_forecast_df[col0].iloc[0].values(),
            *transposed_forecast_df[col0].iloc[1].values(),
            *dict(transposed_forecast_df[col0].iloc[2][0]).values()
        ],
        col1: [
            *transposed_forecast_df[col1].iloc[0].values(),
            *transposed_forecast_df[col1].iloc[1].values(),
            *dict(transposed_forecast_df[col1].iloc[2][0]).values()
        ],
        col2: [
            *transposed_forecast_df[col2].iloc[0].values(),
            *transposed_forecast_df[col2].iloc[1].values(),
            *dict(transposed_forecast_df[col2].iloc[2][0]).values()
        ]
    })
    forecast_df.index = indexes

except Exception as e:
    st.error(f"Failed to fetch or process forecast data: {e}")
    forecast_df = pd.DataFrame()

# --- Streamlit App ---
st.title("Weather Data :tada:")

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
                 A secondary goal of this project is to present global emission data through geo-spatial plots.
                 Upon this, I will perform time series analysis to detect anomalies.
                 """)

with st.container():
    st.title("Current Data for Eltham, UK")
    if not json_df.empty:
        st.dataframe(json_df, use_container_width=True)
    else:
        st.warning("No current weather data available.")

with st.container():
    st.title("Forecast Data For Eltham, UK")
    if not forecast_df.empty:
        st.dataframe(forecast_df, use_container_width=True)
    else:
        st.warning("No forecast data available.")

# --- Greenhouse Classification Model ---
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

    # Encode input values using positional index mapping
    categories = {val: idx for idx, val in enumerate(unique_categories)}
    languages = {val: idx for idx, val in enumerate(unique_languages)}

    input_category = categories[category_input]
    input_language = languages[language_input]

    input_values = np.array([year_input, value_input, input_category, input_language]).reshape(1, -1)
    prediction = model.predict(input_values)

    # Safely convert prediction to index and look up country
    pred_index = int(prediction[0])
    if 0 <= pred_index < len(unique):
        country_prediction = unique[pred_index]
    else:
        country_prediction = "Unknown (prediction out of range)"

    st.write(f"Prediction ID: {pred_index}")
    st.write(f"Country Prediction: {country_prediction}")

with explanation_tab:
    st.header("Model Explanation with SHAP")

    # Extract raw numpy array from SHAP Explanation object if necessary
    raw_shap = shap_values.values if hasattr(shap_values, 'values') else shap_values

    # Handle both 2D (binary/regression) and 3D (multiclass) SHAP value arrays
    shap_values_to_plot = raw_shap[:, :, 0] if raw_shap.ndim == 3 else raw_shap
    st_shap(shap.summary_plot(shap_values_to_plot, X_test))

# --- Greenhouse Emission Analysis ---
st.write("\n \n \n")
with st.container():
    st.title("Greenhouse Emission Analysis")
    option = st.selectbox("Which Country would You like to visualize?", unique)
    st.write("Current Option: " + option)
    hopefully_works = pd.read_csv("data/greenhouse.csv")
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

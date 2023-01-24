import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import requests
file = open("locationID.csv", "r")
x1 = []
y1 = []

for i in range(-10, 11):
    x1.append(i)
    y1.append(i**2)
df = pd.DataFrame({
    "x": x1,
    "y": y1
})
locationID_hourly = requests.get("http://datapoint.metoffice.gov.uk/public/data/val/wxobs/all/json/sitelist?key=0d75cc84-e06a-4632-8bd2-b1cf041e7b09")

df1 = pd.read_csv("~/locationID.csv")
df1 = df1.fillna("0")


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

with st.container():
    st.line_chart(df)
with st.container():
    st.title("Location Data for the UK")
    st.write(df1.head())

        
        

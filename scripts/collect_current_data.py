#!/usr/bin/env python3

import requests
import pandas as pd 
import json 
import os 
import datetime 
import sys
import streamlit as st 
import time
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# I could 
try: 
    weather_api_key = sys.argv[1]
except Exception as e: 
    print (f"There was an exception: {e}")

now = datetime.datetime.now()
localtime = f"{now.day}-{now.month}-{now.year}"

current = requests.get(f"http://api.weatherapi.com/v1/current.json?key={weather_api_key}&q=London&aqi=yes")
weather_data = pd.read_json(current.text)
def clean_data(data):
    """
    putting the columns together as they do not overlap.
    """
    print ("----------- DATA")
    print (data) 
    values = [*data['location'], *data['current']]
    df = pd.Series(values)
    

    print ("----------- Cleaning the dataset")
    cleaned_values = df.dropna().tolist()
    data[f"{localtime}"] = cleaned_values
    data.drop(['location', 'current'], axis=1, inplace=True)
    print ("----------- FORMATTED DATASET") 
    print (data.head()) 
    print ("----------- Saving the dataset") 
    data.to_csv(f"{BASE_DIR}/collected_data/{localtime}.csv")

try: 
    clean_data(weather_data)
except Exception as e: 
    print (f"Error: ") 
    print ("----------------------------")
    print (e) 
    print ("----------------------------")
    
finally: 
    print ("Finished")

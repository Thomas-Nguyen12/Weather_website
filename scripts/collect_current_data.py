#!/usr/bin/env python3

import requests
import pandas as pd 
import json 
import os 
import datetime 
import sys
from dotenv import load_dotenv
import streamlit as st 
import time
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# I could 
load_dotenv() 
try: 

    weather_api_key = os.getenv("current_api_key") 
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
    values = [*data.location, *data.current]
    df = pd.Series(values)
    cleaned_values = df.dropna().tolist()
    data[new_column] = cleaned_values
    data.drop(['location', 'current'], axis=1, inplace=True)
    data.to_csv(f"{BASE_DIR}/collected_data/{localtime}.csv")
    print (data)
    
try: 
    clean_data(weather_data)
except Exception as e: 
    print (f"Error: ") 
    print ("----------------------------")
    print (e) 
    print ("----------------------------")
    
finally: 
    print ("Finished")

#!/usr/bin/env python3

import requests
import pandas as pd 
import json 
import os 
import datetime 
import sys

sys.path.append("/Users/thomasnguyen/")
import api_keys


current = requests.get(f"http://api.weatherapi.com/v1/current.json?key={api_keys.weather_api_key}&q=London&aqi=yes")
weather_data = pd.read_json(current.text)
def clean_data(data):
    """
    putting the columns together as they do not overlap.
    """
    values = [*data.location, *data.current]
    df = pd.Series(values)
    cleaned_values = df.dropna().tolist()
    
    # the new column should have the date 
    new_column = data.loc['localtime'][0]

    data[new_column] = cleaned_values
    data.drop(['location', 'current'], axis=1, inplace=True)
    data.to_csv(f"~/weather_website/collected_data/{new_column}.csv")
    print (data)
    
try: 
    clean_data(weather_data)
except Exception as e: 
    print (f"Error: ") 
    print ("----------------------------")
    print (e) 
    print ("----------------------------")
    
print ("Finished")

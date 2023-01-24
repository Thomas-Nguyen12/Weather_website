import requests
import re
import pandas as pd

# This will return a list of locations for which results are available for the hourly observations data feed
locationID_hourly = requests.get("http://datapoint.metoffice.gov.uk/public/data/val/wxobs/all/json/sitelist?key=0d75cc84-e06a-4632-8bd2-b1cf041e7b09")

locationID_daily = requests.get("http://datapoint.metoffice.gov.uk/public/data/val/wxfcs/all/json/sitelist?key=0d75cc84-e06a-4632-8bd2-b1cf041e7b09")



df = pd.read_json(locationID_hourly.text)
df1 = pd.read_json(locationID_daily.text)

file = open("locationID_hourly.txt", "w")
file.write(df.to_string())
file.close()

file1 = open("locationID_daily.txt", "w")
file1.write(df1.to_string())
file1.close()


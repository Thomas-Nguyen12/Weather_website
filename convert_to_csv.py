import pandas as pd
import requests 
import time 
import csv
import mysql.connector
import datetime

localtime = time.asctime(time.localtime(time.time()) )

day = datetime.datetime.now().day 
month = datetime.datetime.now().month
year = datetime.datetime.now().year 

time = f"{day}{month}{year}"

current = requests.get("http://api.weatherapi.com/v1/current.json?key=4a1f9e155ac6494e98a15506222712&q=London&aqi=yes") 
current_df = pd.read_json(current.text)

current_df["category"] = current_df.index

## Changing index values
current_df.index = [i for i in range(len(current_df))]

current_df.to_csv(f"~/weather_files/{time}.csv")
df = pd.read_csv(f"~/weather_files/{time}.csv")

### Uploading csv files to sql database
### I need to create a new table each time
# Example usage

host_name = "sql8.freesqldatabase.com"
database_name = "sql8624952"
user_name = "sql8624952"
password_name = "6glrRxLFYx"



mydb = mysql.connector.connect(
    host=host_name,
    database=database_name,
    user = user_name,
    password=password_name,
)

mycursor = mydb.cursor()

mycursor.execute("CREATE TABLE weather_table1 (id INTEGER PRIMARY KEY, location TEXT, current TEXT, category TEXT);")

#mycursor.execute("CREATE TABLE weather_table2 (id INTEGER primary key, location TEXT, current TEXT, category TEXT);")
for i in range(len(current_df)):
    location1 = current_df.iloc[i][0]
    current1 = current_df.iloc[i][1]
    category1 = current_df.iloc[i][2]
    mycursor.execute("INSERT INTO weather_table1 (id, location, current, category) values ((%s, %s, %s, %s));" % (i, location1, current1, category1))
    mycursor.commit()
    
import pandas as pd
import datetime
import numpy as np
import mysql.connector

now = datetime.datetime.now()

## Importing data
current = requests.get("http://api.weatherapi.com/v1/current.json?key=4a1f9e155ac6494e98a15506222712&q=London&aqi=yes")

df = pd.read_json(current.text)                                                                        
print ('\n \n')
## Reformatting dataset
values = df.values
values = np.reshape(values, (2, 32))
new_df = pd.DataFrame(values, columns=df.index)
indexes = ["location:" + str(now.day) + "/" + str(now.month) + "/" + str(now.year), "current:" + str(now.day) + "/" + str(now.month) + "/" + str(now.year)]


new_df.rename({"localtime_epoch": "epoch",
    "localtime": "time",
    "condition": "weather_condition"},
    axis=1, inplace=True)

new_df.drop(["weather_condition"], axis=1, inplace=True)
# There is a value error here somehow
new_df.insert(0, "id", indexes)
print ("new df")
print (new_df)
print ("\n \n \n \n \n \n \n")
array = []
keys = list(new_df.iloc[1].air_quality.keys())
values = list(new_df.iloc[1].air_quality.values())
for i in range(len(keys)):
    print (keys[i] + str(values[i]))
    array.append(keys[i] + str(values[i]))

array = ''.join(array)
print (array)
print ("\n \n \n \n")
## I need to replace the value of new_df.iloc[1].air_quality with array
value = new_df.iloc[1].air_quality
new_df.replace(value, array, inplace=True) 


print (new_df.air_quality)
print ("\n \n \n \n \n")
mydb = mysql.connector.connect(
    host="sql8.freesqldatabase.com",
    user="sql8639994",
    password="JYYat3pQfJ",
    database="sql8639994"
)

mycursor = mydb.cursor()



# I believe the dictionary list within "Air quality" is causing the "Not enough parameters" issue
for index, row in new_df.iterrows():
    values_row = tuple(str(value) for value in row)  # Convert row values to strings
    print (values_row)
    query = """
    
        INSERT INTO weather_data (
            id, name, region, country, lat, lon, tz_id, epoch, time, last_updated_epoch, last_updated, temp_c, temp_f,
            is_day, wind_mph, wind_kph, wind_degree, wind_dir, pressure_mb, pressure_in,
            precip_mm, precip_in, humidity, cloud, feelslike_c, feelslike_f, vis_km, vis_miles, uv, gust_mph, gust_kph, air_quality
        )
        VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
    """
    try:
        mycursor.execute(query, values_row)
        mydb.commit()
        print("Row inserted successfully")
    except Exception as e:
        print("Error:", e)
        mydb.rollback()  # Rollback in case of an error



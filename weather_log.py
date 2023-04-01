import requests
import time

current = requests.get("http://api.weatherapi.com/v1/current.json?key=4a1f9e155ac6494e98a15506222712&q=London&aqi=yes")

localtime = time.asctime(time.localtime(time.time()) )

weather_file = open(localtime + "json", "w")
weather_file.write(current.text)
weather_file.close()

## hopefully this works!

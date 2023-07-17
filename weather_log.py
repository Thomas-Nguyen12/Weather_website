import requests
import time

current = requests.get("http://api.weatherapi.com/v1/current.json?key=4a1f9e155ac6494e98a15506222712&q=London&aqi=yes")

localtime = time.asctime(time.localtime(time.time()) )

with open('/Users/thomasnguyen/weather_files/' + localtime + ".json", 'w') as weather_file:
    weather_file.write(current.text)
    weather_file.close()

## hopefully this works!

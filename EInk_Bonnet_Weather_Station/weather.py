"""
This example queries the Open Weather Maps site API to find out the current
weather for your location... and display it on a eInk Bonnet!
"""

import time
import urllib.request
import urllib.parse
import digitalio
import busio
import board
from adafruit_epd.ssd1675 import Adafruit_SSD1675
from weather_graphics import Weather_Graphics
from bluepy import btle

# function to process the data from BLE local_sensor service data into proper formatting 
def converter(data):
    data = str(data)
    print("Raw data: {}".format(data))
    data = data.strip('b')
    data = data.strip("'")
    data = data.strip('\\r\\n')
    data = data.strip("x")
    data = int(data, 16)

    return data
# Initializing SPI pins for the E ink display
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
ecs = digitalio.DigitalInOut(board.CE0)
dc = digitalio.DigitalInOut(board.D22)
rst = digitalio.DigitalInOut(board.D27)
busy = digitalio.DigitalInOut(board.D17)

# You'll need to get a token from openweathermap.org, looks like:
# 'b6907d289e10d714a6e88b30761fae22'
OPEN_WEATHER_TOKEN = ""

# Use cityname, country code where countrycode is ISO3166 format.
# E.g. "New York, US" or "London, GB"
LOCATION = "NASHVILLE, US"
DATA_SOURCE_URL = "http://api.openweathermap.org/data/2.5/weather"

if len(OPEN_WEATHER_TOKEN) == 0:
    raise RuntimeError(
        "You need to set your token first. If you don't already have one, you can register for a free account at https://home.openweathermap.org/users/sign_up"
    )

# Set up where we'll be fetching data from
params = {"q": LOCATION, "appid": OPEN_WEATHER_TOKEN}
data_source = DATA_SOURCE_URL + "?" + urllib.parse.urlencode(params)

# Initialize the Display
display = Adafruit_SSD1675(
    122, 250, spi, cs_pin=ecs, dc_pin=dc, sramcs_pin=None, rst_pin=rst, busy_pin=busy,
)

display.rotation = 1
# Creating an Graphics object that performs our draw function
gfx = Weather_Graphics(display, am_pm=True, celsius=True)
weather_refresh = None

# Performing a URL Pull Request from the weather API
response = urllib.request.urlopen(data_source)

# Connecting to our BLE local temperature and humidity sensor

print("Connecting....")
device = btle.Peripheral("E6:3C:45:7D:D5:2C") # peripheral device MAC ADDRESS
local_sensor = btle.UUID("190f") # The UUID of the entire btle service broadcast
local_service = device.getServiceByUUID(local_sensor)
temperature_uuid = btle.UUID("2b19")
humidity_uuid = btle.UUID("2c19")
temp_value = local_service.getCharacteristics(temperature_uuid)[0]
humidity_value = local_service.getCharacteristics(humidity_uuid)[0] # getting sensor data from the BLE characteristics
temp_int = converter(temp_value.read())
humidity_int = converter(humidity_value.read())
# Checking if we get a valid response
if response.getcode() == 200:
    value = response.read()
    print("Response is", value)
    print(f"The local temperature is: {str(temp_int)}")
    gfx.display_weather(value, temp_int)
    weather_refresh = time.monotonic()
else:
    print("Unable to retrieve data at {}".format(response))

gfx.update_time()

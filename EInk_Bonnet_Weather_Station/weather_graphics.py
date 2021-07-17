from datetime import datetime
import json
from PIL import Image, ImageDraw, ImageFont
from adafruit_epd.epd import Adafruit_EPD

small_font = ImageFont.truetype(
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16
)
medium_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 18)
large_font = ImageFont.truetype(
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 44
)
icon_font = ImageFont.truetype("/usr/share/fonts/truetype/meteocon/meteocons.ttf", 36)

# Map the OpenWeatherMap icon code to the appropriate font character
# See http://www.alessioatzeni.com/meteocons/ for icons
ICON_MAP = {
    "01d": "B",
    "01n": "C",
    "02d": "H",
    "02n": "I",
    "03d": "N",
    "03n": "N",
    "04d": "Y",
    "04n": "Y",
    "09d": "Q",
    "09n": "Q",
    "10d": "R",
    "10n": "R",
    "11d": "Z",
    "11n": "Z",
    "13d": "W",
    "13n": "W",
    "50d": "J",
    "50n": "K",
}

# RGB Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class Weather_Graphics:
    def __init__(self, display, *, am_pm=True, celsius=True):
        self.am_pm = am_pm
        self.celsius = celsius

        self.small_font = small_font
        self.medium_font = medium_font
        self.large_font = large_font

        self.display = display

        self._weather_icon = None
        self._city_name = None
        self._main_text = None
        self._temperature = None
        self._description = None
        self._clothes = None
        self._time_text = None
        self._feels_like = None
        

    def display_weather(self, weather):
        weather = json.loads(weather.decode("utf-8"))

        # set the icon/background
        self._weather_icon = ICON_MAP[weather["weather"][0]["icon"]]

        city_name = weather["name"]
        print(city_name)
        self._city_name = city_name

        main = weather["weather"][0]["main"]
        print(main)
        self._main_text = main

        temperature = weather["main"]["temp"] - 273.15  # its...in kelvin
        feels_like =  weather["main"]["feels_like"] - 273.15
        print(temperature)
        print("feels like: " + str(feels_like))
        if self.celsius:
            self._temperature = "%d °C" % temperature
            self._feels_like = "%d °C" % feels_like
        else:
            self._temperature = "%d °F" % ((temperature * 9 / 5) + 32)
            self._feels_like = "%d °C" % ((feels_like * 9 / 5) + 32)

        description = weather["weather"][0]["description"]
        description = description[0].upper() + description[1:]
        print(description)
        self._description = description
        if temperature > 20:
            clothes = "Shorts Weather"
            self._clothes = clothes
        elif temperature > 15 and temperature < 20:
            clothes = "Hoodie day"
            self._clothes = clothes
        elif temperature > 10  and temperature < 15:
            clothes = "Thick Hoodie"
            self._clothes = clothes
        elif temperature > 5 and temperature < 10:
            clothes = "Jacket and hoodie"
            self._clothes = clothes
        elif temperature > -5  and  temperature < 5:
            clothes = "Jacket and thick hoodie"
            self._clothes = clothes
        else:
            clothes = "Heavy Jacket"
            self._clothes = clothes
        print(clothes)
        # "thunderstorm with heavy drizzle"
        print("height: " + str(self.display.height))
        print("width: " + str(self.display.width))

        self.update_time()

    def update_time(self):
        now = datetime.now()
        self._time_text = now.strftime("%I:%M %p").lstrip("0").replace(" 0", " ")
        self.update_display()

    def update_display(self):
        self.display.fill(Adafruit_EPD.WHITE)
        image = Image.new("RGB", (self.display.width, self.display.height), color=WHITE)
        draw = ImageDraw.Draw(image)

        # Draw the Icon
        (font_width, font_height) = icon_font.getsize(self._weather_icon)
        print("font width: " + str(font_width) + "font_height: " + str(font_height))
        draw.text(
            (
                self.display.width - font_width // 2 - 40 ,
                self.display.height - font_height // 2 - 65,
            ),
            self._weather_icon,
            font=icon_font,
            fill=BLACK,
        )

        # Draw the city
        draw.text(
            (1, 1), self._city_name, font=self.medium_font, fill=BLACK,
        )

        # Draw the time
        (font_width, font_height) = medium_font.getsize(self._time_text)
        print("time font width: " + str(font_width) + "font_height: " + str(font_height))
        draw.text(
            (1, font_height * 2 - 16),
            self._time_text,
            font=self.medium_font,
            fill=BLACK,
        )

        # Draw the feels like
        (font_width, font_height) = medium_font.getsize(self._feels_like)
        print("feels like font width: " + str(font_width) + "font_height: " + str(font_height))
        draw.text(
            (1, self.display.height - font_height * 5 + 10),
            "feels like: " + self._feels_like,
            font=self.medium_font,
            fill=BLACK,
        )

        # Draw the description
        (font_width, font_height) = small_font.getsize(self._description)
        print("desc font width: " + str(font_width) + "font_height: " + str(font_height))
        draw.text(
            (5, self.display.height - font_height - 7),
            self._description,
            font=self.medium_font,
            fill=BLACK,
        )

        # Draw the temperature
        (font_width, font_height) = large_font.getsize(self._temperature)
        print("temp font width: " + str(font_width) + "font_height: " + str(font_height))
        draw.text(
            (
                self.display.width - font_width - 5,
                self.display.height - font_height * 3,
            ),
            self._temperature,
            font=self.large_font,
            fill=BLACK,
        )

        (font_width, font_height) = small_font.getsize(self._clothes)
        print("clothes font width: " + str(font_width) + "font_height: " + str(font_height))
        draw.text(
            (1, self.display.height - font_height - 30),
            self._clothes,
            font=self.medium_font,
            fill=BLACK,
        )
        self.display.image(image)
        self.display.display()

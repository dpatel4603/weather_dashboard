import sys

import requests
from geopy.geocoders import Nominatim
import datetime

geolocator = Nominatim(user_agent="weather_api_call")
date = datetime.date.today()


def get_location():
    location_confirmation = "no"
    while location_confirmation == "no":
        try:
            location_call = input("What is the American address of where you want the weather forecast?\n")
            location = geolocator.geocode(location_call)
            print(location.address)
            location_confirmation = input("Is the following address correct? type yes or no: ")
            location_confirmation.lower()
            latitude = location.latitude
            longitude = location.longitude

        except AttributeError:
            print("INVALID ADDRESS")
            break

        return latitude, longitude


def get_weather(latitude, longitude):
    response = requests.get(f"https://api.weather.gov/points/{latitude},{longitude}")
    data = response.json()

    how_many_days = input("How many days do you want to find the weather for, limit is one week?\n")

    # Step 2: Extract the forecast URL
    try:
        forecast_url = data['properties']['forecast']

    except KeyError:
        print("INVALID FORECAST")
        sys.exit()
    # Step 3: Get the detailed forecast
    forecast_response = requests.get(forecast_url)
    forecast_data = forecast_response.json()
    for i in range(int(how_many_days) * 2):
        print(f"{forecast_data['properties']['periods'][i]['name']} the weather will be "
              f"{forecast_data['properties']['periods'][i]['detailedForecast']}")


def main():
    latitude, longitude = get_location()
    get_weather(latitude, longitude)


if __name__ == "__main__":
    main()

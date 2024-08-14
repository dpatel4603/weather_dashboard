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
            if location is None:
                print("INVALID ADDRESS")
                continue
            print(location.address)
            location_confirmation = input("Is the following address correct? type yes or no: ")
            location_confirmation = location_confirmation.lower()
            if location_confirmation == "yes":
                latitude = location.latitude
                longitude = location.longitude
                return latitude, longitude

        except AttributeError:
            print("INVALID ADDRESS")
            continue


def get_weather(latitude, longitude):
    try:
        response = requests.get(f"https://api.weather.gov/points/{latitude},{longitude}")
        response.raise_for_status()  # Raises HTTPError if the request returned an unsuccessful status code
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from weather.gov: {e}")
        sys.exit()

    while True:
        try:
            how_many_days = int(input("How many days do you want to find the weather for? (Limit is one week)\n"))
            if 1 <= how_many_days <= 7:
                break
            else:
                print("Please enter a number between 1 and 7.")
        except ValueError:
            print("Please enter a valid number.")

    try:
        forecast_url = data['properties']['forecast']
    except KeyError:
        print("INVALID FORECAST DATA")
        sys.exit()

    try:
        forecast_response = requests.get(forecast_url)
        forecast_response.raise_for_status()
        forecast_data = forecast_response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching forecast data: {e}")
        sys.exit()

    for i in range(int(how_many_days) * 2):
        period = forecast_data['properties']['periods'][i]
        print(f"{period['name']}: {period['detailedForecast']}")


def main():
    latitude, longitude = get_location()
    if latitude and longitude:
        get_weather(latitude, longitude)


if __name__ == "__main__":
    main()

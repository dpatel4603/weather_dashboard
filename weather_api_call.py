import requests
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="weather_api_call")


def get_location():
    location_confirmation = "no"
    while location_confirmation == "no":
        location_call = input("What is the address of where you want the weather forecast?\n")
        location = geolocator.geocode(location_call)
        print(location.address)
        location_confirmation = input("Is the following address correct? type yes or no: ")
        location_confirmation.lower()
        latitude = location.latitude
        longitude = location.longitude

    return latitude, longitude


def get_weather(latitude, longitude):
    response = requests.get(f"https://api.weather.gov/points/{latitude},{longitude}")
    data = response.json()

    # Step 2: Extract the forecast URL
    forecast_url = data['properties']['forecast']

    # Step 3: Get the detailed forecast
    forecast_response = requests.get(forecast_url)
    forecast_data = forecast_response.json()
    return (f"{forecast_data['properties']['periods'][1]['name']} the weather will be "
            f"{forecast_data['properties']['periods'][1]['detailedForecast']}")


def main():
    latitude, longitude = get_location()
    weather = get_weather(latitude, longitude)
    print(weather)


if __name__ == "__main__":
    main()

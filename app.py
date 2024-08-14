# Sets up the imports for this project
from flask import Flask, render_template, request
import requests
from geopy.geocoders import Nominatim

# Sets up the Flask Application
app = Flask(__name__)

# Sets up the library that utilizes the Nominatim API for GeoLocation
geolocator = Nominatim(user_agent="weather_api_call")


# Creates the function that outputs the Latitude and Longitude of an American Street Address
def get_location(location_call):
    try:
        location = geolocator.geocode(location_call)
        if location is None:
            return None, None
        return location.latitude, location.longitude
    except Exception as e:
        print(f"Error getting location: {e}")
        return None, None


# Creates the function that gets the weather based off the latitude and longitude
# and for length of forecast
def get_weather(latitude, longitude, days):
    try:
        response = requests.get(f"https://api.weather.gov/points/{latitude},{longitude}")
        response.raise_for_status()
        data = response.json()
        forecast_url = data['properties']['forecast']
        forecast_response = requests.get(forecast_url)
        forecast_response.raise_for_status()
        forecast_data = forecast_response.json()
        periods = forecast_data['properties']['periods'][:int(days) * 2]
        return periods
    except requests.exceptions.RequestException as e:
        print(f"Error fetching forecast data: {e}")
        return None


# Main method that sets up the flask application
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        location = request.form.get('location')
        days = request.form.get('days')
        latitude, longitude = get_location(location)
        if latitude and longitude:
            forecast = get_weather(latitude, longitude, days)
            if forecast:
                return render_template('result.html', forecast=forecast, location=location)
        return render_template('index.html', error="Invalid address or forecast data")
    return render_template('index.html')


# Main call that runs the application, debug is on
if __name__ == "__main__":
    app.run(debug=True)

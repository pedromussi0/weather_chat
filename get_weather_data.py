import os
import requests
from dotenv import load_dotenv
import geocoder
import json

geocoding_api_key = os.getenv("GEOCODING_API_KEY")

def get_current_location():
    g = geocoder.ip('me')
    return g.city

def get_coordinates(location=None):
    if location is None:
        location = get_current_location()
    
    api_endpoint = "https://maps.googleapis.com/maps/api/geocode/json"
    api_key = geocoding_api_key

    parameters = {
        "address": location,
        "key": api_key
    }

    try:
        response = requests.get(api_endpoint, params=parameters)
        response.raise_for_status()  
        geocoding_data = response.json()

        if geocoding_data["status"] == "OK":
            results = geocoding_data["results"]
            first_result = results[0]
            geometry = first_result["geometry"]
            location = geometry["location"]
            latitude = location["lat"]
            longitude = location["lng"]

            return latitude, longitude
        else:
            print("Geocoding API error:", geocoding_data["status"])
            return None
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return None

def get_uv_radiation(location=None):
    if location is None:
        location = get_current_location()
    
    latitude, longitude = get_coordinates(location)

    api_endpoint = "https://api.open-meteo.com/v1/forecast"
    parameters = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "uv_index",
        "daily": "uv_index_max",
        "forecast_days": 1,
        "timezone": "auto",
    }

    try:
        response = requests.get(api_endpoint, params=parameters)
        response.raise_for_status()  # Raise an exception if the request was not successful
        weather_data = response.json()

        hourly_uv_index = weather_data["hourly"]["uv_index"]
        return json.dumps(hourly_uv_index)
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return None

def get_rain_precipitation(location=None):
    if location is None:
        location = get_current_location()
    
    latitude, longitude = get_coordinates(location)

    api_endpoint = "https://api.open-meteo.com/v1/forecast"
    parameters = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "precipitation",
        "daily": "precipitation_sum",
        "forecast_days": 1,
        "timezone": "auto",
    }

    try:
        response = requests.get(api_endpoint, params=parameters)
        response.raise_for_status()  # Raise an exception if the request was not successful
        weather_data = response.json()

        hourly_precipitation = weather_data["hourly"]["precipitation"]
        return json.dumps(hourly_precipitation)
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return None


location = 'florianopolis'
print (get_uv_radiation(location))

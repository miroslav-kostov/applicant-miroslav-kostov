import requests
import time
import json
import os
from open_weather_authorization import access_secret

def get_lat_lon(city_name, country_code="US", api_key="", state=None):
    base_url = "http://api.openweathermap.org/geo/1.0/direct"
    q = f"{city_name},{country_code}" if not state else f"{city_name},{state},{country_code}"
    
    params = {
        "q": q,
        "limit": 1,
        "appid": api_key
    }

    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data:
            return {
                "city_name": city_name,
                "state": state,
                "lat": data[0]["lat"],
                "lon": data[0]["lon"]
            }
        else:
            print(f"No result found for {q}")
    else:
        print(f"Failed to fetch geocode for {q}, status: {response.status_code}")

    return None

def get_coordinates_for_cities(cities, api_key):
    results = []
    for city, state in cities:
        result = get_lat_lon(city, state=state, api_key=api_key)
        if result:
            results.append(result)
        time.sleep(1)
    return results

def save_to_json(data, filepath):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Coordinates saved to {filepath}")

if __name__ == "__main__":
    project = "open-weather-miroslav-kostov"
    secret_name = "open-weather-api-key"
    api_key = access_secret(secret_name, project)

    cities = [
        ("Sioux Falls", "South Dakota"),
        ("Great Falls", "Montana"),
        ("Houghton", "Michigan"),
        ("Fargo", "North Dakota"),
        ("Duluth", "Minnesota"),
        ("Bismarck", "North Dakota"),
        ("Aberdeen", "South Dakota"),
        ("Grand Island", "Nebraska"),
        ("Glasgow", "Montana"),
        ("Omaha", "Nebraska"),
        ("Portland", "Oregon"),
    ]
    coordinates = get_coordinates_for_cities(cities, api_key)

    output_path = "etl_pipeline/city_coordinates.json"
    save_to_json(coordinates, output_path)

from open_weather_authorization import access_secret

import requests
import time
from typing import Optional, Dict

class OpenWeatherClient:
    def __init__(self, api_key: str, retries: int = 3, backoff_factor: float = 1.0):
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/3.0/onecall/timemachine"
        self.retries = retries
        self.backoff_factor = backoff_factor

    def get_historical_weather(
        self,
        lat: float,
        lon: float,
        dt: int,
        units: str = "metric",
        lang: str = "en"
    ) -> Optional[Dict]:
        """
        Get historical weather data for a specific location and time.

        :param lat: Latitude of the location
        :param lon: Longitude of the location
        :param dt: Unix timestamp (must be in the past)
        :param units: Units of measurement. standard, metric, imperial
        :param lang: Language for weather description
        :return: JSON response as a dictionary
        """
        params = {
            "lat": lat,
            "lon": lon,
            "dt": dt,
            "appid": self.api_key,
            "units": units,
            "lang": lang,
        }

        for attempt in range(1, self.retries + 1):
            try:
                response = requests.get(self.base_url, params=params, timeout=10)
                response.raise_for_status()
                return response.json()
            except requests.RequestException as e:
                print(f"[Attempt {attempt}] Error: {e}")
                if attempt < self.retries:
                    time.sleep(self.backoff_factor * attempt)
                else:
                    print("Max retries reached. Failing.")
                    return None


if __name__ == "__main__":
    # Example: Fargo, North Dakota
    latitude = 46.8772
    longitude = -96.7898
    # Date: Jan 1, 2024 → 1704067200 (Unix timestamp in UTC)
    timestamp = int(time.mktime(time.strptime("2024-01-01", "%Y-%m-%d")))

    project = "open-weather-miroslav-kostov"
    secret_name = "open-weather-api-key"
    api_key = access_secret(secret_name, project)

    client = OpenWeatherClient(api_key)

    weather_data = client.get_historical_weather(lat=latitude, lon=longitude, dt=timestamp)

    if weather_data:
        print(weather_data)

    #  print(int(time.mktime(time.strptime("2025-04-15", "%Y-%m-%d"))))
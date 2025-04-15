import time
import requests
import json
from datetime import datetime, timedelta
from google.cloud import bigquery
from open_weather_authorization import access_secret

class OpenWeatherClient:
    def __init__(self, retries: int = 3, backoff_factor: float = 1.0):
        self.project_id = "open-weather-miroslav-kostov"
        self.secret_name = "open-weather-api-key"
        self.api_key = access_secret(self.secret_name, self.project_id)
        self.base_url = "https://api.openweathermap.org/data/3.0/onecall/day_summary"
        self.coordinates_url = "http://api.openweathermap.org/geo/1.0/direct"
        self.retries = retries
        self.backoff_factor = backoff_factor
        self.cities_input_list = [
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

    def get_historical_weather(self, lat, lon, date, units="metric", lang="en"):
        params = {
            "lat": lat,
            "lon": lon,
            "date": date,
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

    def get_lat_lon(self, city_name, country_code="US", state=None):
        q = f"{city_name},{country_code}" if not state else f"{city_name},{state},{country_code}"
        params = {
            "q": q,
            "limit": 1,
            "appid": self.api_key
        }
        response = requests.get(self.coordinates_url, params=params)
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

    def get_coordinates_for_cities(self, cities=None):
        if not cities:
            cities = self.cities_input_list
        results = []
        for city, state in cities:
            result = self.get_lat_lon(city, state=state)
            if result:
                results.append(result)
            time.sleep(1)
        return results

    def fetch_and_load_historic_data(self, cities=None, start_date=None, end_date=None, table_name=None):
        if not cities:
            cities = self.get_coordinates_for_cities()

        # If no start date is specified, run yesterday's data
        if not start_date:
            start_date = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")
        # If no end_date is specified, same as start_date
        if not end_date:
            end_date = start_date

        if not table_name:
            table_name = "mk_openweather_historic"

        curr_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date_dt = datetime.strptime(end_date, "%Y-%m-%d").date()

        bq_client = bigquery.Client(project=self.project_id)
        table_id = f"{self.project_id}.open_weather.{table_name}"

        rows_to_insert = []

        while curr_date <= end_date_dt:
            for city in cities:
                weather_data = self.get_historical_weather(
                    lat=city["lat"],
                    lon=city["lon"],
                    date=curr_date
                )
                if weather_data:
                    row_dict = {
                        "city_name": city["city_name"],
                        "state": city.get("state"),
                        "date": weather_data.get("date"),
                        "lat": weather_data.get("lat"),
                        "lon": weather_data.get("lon"),
                        "tz": weather_data.get("tz"),
                        "units": weather_data.get("units"),
                        "cloud_cover_afternoon": weather_data.get("cloud_cover", {}).get("afternoon"),
                        "humidity_afternoon": weather_data.get("humidity", {}).get("afternoon"),
                        "precipitation_total": weather_data.get("precipitation", {}).get("total"),
                        "temp_min": weather_data.get("temperature", {}).get("min"),
                        "temp_max": weather_data.get("temperature", {}).get("max"),
                        "temp_afternoon": weather_data.get("temperature", {}).get("afternoon"),
                        "temp_night": weather_data.get("temperature", {}).get("night"),
                        "temp_evening": weather_data.get("temperature", {}).get("evening"),
                        "temp_morning": weather_data.get("temperature", {}).get("morning"),
                        "pressure_afternoon": weather_data.get("pressure", {}).get("afternoon"),
                        "wind_max_speed": weather_data.get("wind", {}).get("max", {}).get("speed"),
                        "wind_max_direction": weather_data.get("wind", {}).get("max", {}).get("direction"),
                    }
                    rows_to_insert.append(row_dict)
            curr_date += timedelta(days=1)

        errors = bq_client.insert_rows_json(table_id, rows_to_insert)
        if errors:
            print(f"Encountered errors while inserting rows: {errors}")
        else:
            print(f"Successfully inserted {len(rows_to_insert)} rows into {table_id}")
        return len(rows_to_insert)



if __name__ == "__main__":
    # client = OpenWeatherClient()
    # start_date = "2024-01-01"
    # end_date = "2024-01-07"
    # table_name = "mk_openweather_historic_jan_2024"
    # print(client.fetch_and_load_historic_data(start_date=start_date, end_date=end_date))
    # client.fetch_and_load_historic_data()
    pass
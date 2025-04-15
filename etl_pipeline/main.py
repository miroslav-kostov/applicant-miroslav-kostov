import functions_framework
import json
from open_weather_api import OpenWeatherClient


@functions_framework.http
def hello_http(request):
    """
    No arguments needed, pulls by default yesterday's data through the script.
    """
    client = OpenWeatherClient()
    inserted_count = client.fetch_and_load_historic_data()
    return (json.dumps({"inserted_rows_count": inserted_count}), 200, {"Content-Type": "application/json"})
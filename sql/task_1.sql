-- Table in BigQuery mk_cities_average_temp

SELECT
    city_name,
    state,
    AVG((temp_min + temp_max)/2) AS avg_temp,
    AVG((temp_afternoon + temp_night + temp_evening + temp_morning)/4) AS avg_temp_by_daytime
FROM `open-weather-miroslav-kostov.open_weather.mk_openweather_historic_jan_2024`
GROUP BY city_name, state
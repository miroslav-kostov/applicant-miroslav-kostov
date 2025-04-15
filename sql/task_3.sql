-- Table in BigQuery mk_pct_cities_per_state_with_rain

WITH city_rain AS (
  SELECT
    date,
    city_name,
    state,
    MAX(CASE WHEN precipitation_total > 0 THEN 1 ELSE 0 END) AS had_any_rain
  FROM `open-weather-miroslav-kostov.open_weather.mk_openweather_historic_jan_2024`
  GROUP BY date, city_name, state
)
SELECT
  date,
  state,
  100 * AVG(had_any_rain) AS pct_cities_with_rain
FROM city_rain
GROUP BY date, state
ORDER BY date ASC, pct_cities_with_rain DESC 
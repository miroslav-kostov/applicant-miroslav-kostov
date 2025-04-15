# Analysis Answers

Below are the SQL queries used to answer the three analysis questions. The historical data resides in the BigQuery tables and in _evidence/tables:


## 1. Provide the average daily temperature for each city in each state.

**Approach**: I created two approaches to get average temp. One by using average of min and max daily temperatures, and the other by using average of all periods of the day.

```sql
-- Table in BigQuery mk_cities_average_temp

SELECT
    city_name,
    state,
    AVG((temp_min + temp_max)/2) AS avg_temp,
    AVG((temp_afternoon + temp_night + temp_evening + temp_morning)/4) AS avg_temp_by_daytime
FROM `open-weather-miroslav-kostov.open_weather.mk_openweather_historic_jan_2024`
GROUP BY city_name, state
```

## 2. Find the top 3 cities with the highest average humidity in each state.

**Approach**: First I created CTE to get avg_humidity for the whole period and then I used window function to rank each city per state based on average humidity.

```sql
-- Table in BigQuery mk_top3_cities_per_state_by_humidity

WITH city_avg_humidity AS (
    SELECT
        city_name,
        state,
        AVG(humidity_afternoon) AS avg_humidity
    FROM `open-weather-miroslav-kostov.open_weather.mk_openweather_historic_jan_2024`
    GROUP BY city_name, state
),

humidity_ranking AS (
    SELECT
        city_name,
        state,
        avg_humidity,
        ROW_NUMBER() OVER (PARTITION BY state ORDER BY avg_humidity DESC) AS rank
    FROM city_avg_humidity
)

SELECT
    city_name,
    state,
    avg_humidity,
    rank
FROM humidity_ranking
WHERE rank <= 3
ORDER BY state, rank
```

## 3. Find the percentage of cities in each state experiencing "rain" as the weather condition.

**Approach**: I used CTE to get which cities had rain and then grouped by date and state to get the percentage of cities per state. I kept daily granularity as with the limited data all states would have 100% of cities with rain.

```sql
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
```
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
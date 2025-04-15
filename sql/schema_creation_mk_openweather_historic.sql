-- This file creates the table `mk_openweather_historic` in the `open_weather` dataset 
-- within the `open-weather-miroslav-kostov` project, following the specified schema.

CREATE TABLE IF NOT EXISTS `open-weather-miroslav-kostov.open_weather.mk_openweather_historic`
(
  city_name STRING,
  state STRING,
  date DATE,
  lat FLOAT64,
  lon FLOAT64,
  tz STRING,
  units STRING,
  cloud_cover_afternoon FLOAT64,
  humidity_afternoon FLOAT64,
  precipitation_total FLOAT64,
  temp_min FLOAT64,
  temp_max FLOAT64,
  temp_afternoon FLOAT64,
  temp_night FLOAT64,
  temp_evening FLOAT64,
  temp_morning FLOAT64,
  pressure_afternoon FLOAT64,
  wind_max_speed FLOAT64,
  wind_max_direction FLOAT64
);

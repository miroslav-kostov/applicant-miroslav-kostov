# README

## Overview
This project implements a daily ETL pipeline that retrieves weather data from the OpenWeather API and stores it in BigQuery for historical analysis. The pipeline leverages Google Cloud Run, Cloud Scheduler, and other GCP services to automate the entire process.

---

## 1. Repository & Setup

1. **Fork & Clone**  
   - Forked the original challenge repository, renamed it to `applicant-miroslav-kostov`, and cloned it locally.

2. **OpenWeather**  
   - Created an account at [openweathermap.org](https://openweathermap.org/) and enabled **One Call API 3.0**.  
   - Obtained an API key.

3. **Google Cloud Project**  
   - Set up a GCP project named `open-weather-miroslav-kostov`.  
   - Enabled relevant services:
     - **Secret Manager** for storing the OpenWeather API key
     - **Cloud Run**, **Cloud Scheduler**, **BigQuery** for the pipeline

4. **Secret Manager**  
   - Stored the OpenWeather API key in Secret Manager under `open-weather-api-key` for secure retrieval.

---

## 2. ETL Pipeline Design

1. **High-Level Approach**  
   - **Cloud Run** hosts and executes a Python ETL script.  
   - **Cloud Scheduler** triggers that service daily to fetch “yesterday’s” data from OpenWeather.

2. **Local Setup**  
   - Installed **Google Cloud CLI** and configured **Application Default Credentials (ADC)** to access GCP services from the local environment.

3. **File Structure & Scripts**  
   - **`open_weather_authorization.py`**: Fetches the API key from GCP’s Secret Manager.
   - **`open_weather_api.py`**:  
     - Includes `get_lat_lon` and `get_coordinates_for_cities` methods to derive lat/lon from city names.  
     - `get_historical_weather` retrieves daily historical data.  
     - `fetch_and_load_historic_data` orchestrates the entire process: loops through cities, retrieves data, and inserts it into BigQuery.  
     - A **MERGE** function could be added for deduplication if needed.
   - **`main.py`**: The Cloud Function (or 2nd-gen Cloud Run function) entry point that creates the client and triggers the pipeline logic.
   - **`requirements.txt`**: Contains Python dependencies (e.g. `requests`, `google-cloud-bigquery`, `google-cloud-secret-manager`).

---

## 3. BigQuery Datasets & Tables

1. **Dataset**  
   - Created a BigQuery dataset called `open_weather`.

2. **Schema Creation**  
   - Used `sql\schema_creation_mk_openweather_historic.sql` to define columns.

3. **Tables**  
   - **`mk_openweather_historic_jan_2024`**: Holds initial data (first week of 2024) pulled locally through the script.  
   - **`mk_openweather_historic`**: Destination table for daily ETL pipeline loads. Initially empty.

---

## 4. Cloud Run & Cloud Scheduler

1. **Cloud Function / Cloud Run**  
   - Deployed a cloud run function named **`openweather-etl-run`** with four files:
     - `requirements.txt`
     - `open_weather_authorization.py`
     - `open_weather_api.py`
     - `main.py`

2. **Cloud Scheduler Job**  
   - Created a job named **`openweather-etl-schedule`** targeting the Cloud Run function’s URL.  
   - Scheduled to run daily at **2 AM**, fetching the previous day’s data from the OpenWeather API and inserting records into BigQuery.

---

## 5. Summary

- The pipeline **automates** daily data ingestion for multiple U.S. cities, storing results in **BigQuery** under the `open_weather` dataset.  
- Potential enhancements:
  - Use **MERGE** logic to manage duplicates and updates.  
  - Add **monitoring/alerting** for pipeline failures.  
  - Expand the solution to handle additional transformations or deeper analyses.

import pandas as pd
import numpy as np
import requests
from datetime import datetime, timedelta
import openmeteo_requests
import requests_cache
from retry_requests import retry
from pandas.tseries.holiday import USFederalHolidayCalendar as calendar
from config import eia_key

# Setup retry logic for requests
cache_session = requests_cache.CachedSession('.cache', expire_after=-1)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)

def fetch_electricity_demand_data(start_date, end_date, eia_key):
    df = []
    url = (f'https://api.eia.gov/v2/electricity/rto/region-data/data/'
           f'?frequency=hourly&data[0]=value&facets[respondent][]=NY&'
           f'facets[type][]=D&start={start_date.strftime("%Y-%m-%dT00")}&'
           f'end={end_date.strftime("%Y-%m-%dT00")}&sort[0][column]=period&'
           f'sort[0][direction]=desc&length=5000&api_key={eia_key}')

    try:
        response = retry_session.get(url)
        response.raise_for_status()  # Raise an error for HTTP codes 4xx/5xx
        data = response.json()['response']['data']
        if data:
            df.append(pd.DataFrame(data))
        else:
            raise ValueError("No data received from API.")
    except requests.RequestException as e:
        raise RuntimeError(f"Request failed: {e}")

    if df:
        demand_hourly = pd.concat(df, ignore_index=True)
        demand_hourly = demand_hourly[['period', 'value']].rename(columns={'period': 'date', 'value': 'demand'})
        demand_hourly['date'] = pd.to_datetime(demand_hourly['date'])
        demand_hourly['date'] = demand_hourly['date'].dt.floor('h')
        return demand_hourly
    else:
        raise RuntimeError("Data fetching was unsuccessful.")

def fetch_weather_data(start_date, end_date):
    openmeteo = openmeteo_requests.Client(session=retry_session)
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": 40.7143,
        "longitude": -74.006,
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": end_date.strftime("%Y-%m-%d"),
        "hourly": "temperature_2m",
        "timezone": "auto"
    }
    try:
        responses = openmeteo.weather_api(url, params=params)
        response = responses[0]
        hourly = response.Hourly()
        hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()

        hourly_data = {"date": pd.date_range(
            start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
            end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=hourly.Interval()),
            inclusive="left"
        )}
        hourly_data["temperature"] = hourly_temperature_2m
        hourly_temperature_dataframe = pd.DataFrame(data=hourly_data)
        hourly_temperature_dataframe['date'] = hourly_temperature_dataframe['date'].dt.tz_localize(None)
        return hourly_temperature_dataframe
    except requests.RequestException as e:
        raise RuntimeError(f"Request failed: {e}")

def merge_and_enrich_data(demand_hourly, hourly_temperature_dataframe):
    if demand_hourly.empty or hourly_temperature_dataframe.empty:
        raise ValueError("Cannot merge data because one of the DataFrames is empty.")

    # Merge data
    demand_hourly.sort_values('date', inplace=True)
    hourly_temperature_dataframe.sort_values('date', inplace=True)
    df = pd.merge(hourly_temperature_dataframe, demand_hourly, on='date', how='inner')

    # Add feature engineering
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['hr'] = df['date'].dt.hour
    df['day_of_week'] = df['date'].dt.dayofweek
    df['is_weekend'] = df['date'].dt.dayofweek >= 5

    holidays = calendar().holidays(start=df['date'].min(), end=df['date'].max())
    df['holiday'] = df['date'].isin(holidays).astype(int)

    # Drop rows with NaN values
    df.dropna(inplace=True)

    return df

def get_recent_data(eia_key):

    end_date = datetime.now()
    # Set the start date to August 1, 2024, at 00:00:00
    start_date = datetime(2024, 8, 1, 0, 0, 0)
    # or  the date range for the last 10 days
    #start_date = end_date - timedelta(days=10)

    try:
        # Fetch data
        demand_hourly = fetch_electricity_demand_data(start_date, end_date, eia_key)
        hourly_temperature_dataframe = fetch_weather_data(start_date, end_date)

        # Merge and enrich data
        df = merge_and_enrich_data(demand_hourly, hourly_temperature_dataframe)
        # Save the DataFrame to a CSV file
        df.to_csv("unseen_data.csv", index=False)
        print(df)
        return df
    except (RuntimeError, ValueError) as e:
        print(f"Error occurred: {e}")
        return

def main():
    get_recent_data(eia_key)

# Run the main function
if __name__ == "__main__":
    main()

import pandas as pd 
import requests
new_observation = {
    'temperature' : 21,
    'year': 2024,
    'month': 8,
    'day': 12,
    'hr': 3,
    'day_of_week': 1,
    'is_weekend': 0,
    'holiday': 0}

url = 'http://localhost:9696/predict'
response = requests.post(url, json=new_observation)

# Check the status code first
if response.status_code == 200:
    try:
        # Attempt to parse the response as JSON
        print(response.json())
    except requests.exceptions.JSONDecodeError:
        # Handle the case where the response is not JSON
        print("Response is not in JSON format. Response content:")
        print(response.text)
else:
    print(f"Request failed with status code: {response.status_code}")
    print("Response content:", response.text)

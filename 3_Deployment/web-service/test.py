import pandas as pd 
import requests

new_observation = {'temperature' :21}

url = 'http://localhost:9696/predict'
response = requests.post(url, json=new_observation)
print(response.json())
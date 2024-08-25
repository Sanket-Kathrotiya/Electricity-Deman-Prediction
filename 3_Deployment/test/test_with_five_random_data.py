import pandas as pd
import requests

# Load the unseen data
unseen_data = pd.read_csv("unseen_data.csv")

# Randomly select 5 observations
sampled_data = unseen_data.sample(n=5)

# Prepare to store the results
results = []

# Loop over each selected observation
for _, row in sampled_data.iterrows():
    new_observation = {
        'temperature': row['temperature'],
        'year': row['year'],
        'month': row['month'],
        'day': row['day'],
        'hr': row['hr'],
        'day_of_week': row['day_of_week'],
        'is_weekend': int(row['is_weekend']),
        'holiday': row['holiday']
    }

    url = 'http://localhost:9696/predict'
    response = requests.post(url, json=new_observation)

    if response.status_code == 200:
        try:
            prediction = response.json()

            demand_key = next(iter(prediction))
            predicted_demand = prediction[demand_key]
            results.append({
                "date": row['date'],
                "predicted_demand": predicted_demand,
                "actual_demand": row['demand']
            })
        except requests.exceptions.JSONDecodeError:
            print("Response is not in JSON format. Response content:")
            print(response.text)
    else:
        print(f"Request failed with status code: {response.status_code}")
        print("Response content:", response.text)

# Print the results
for result in results:
    ###print(f"Date: {result['date']}, Predicted Demand: {int(result['predicted_demand'])} MWh, Actual Demand: {result['actual_demand']} MWh")
    predicted_demand_int = int(result['predicted_demand'])
    actual_demand = result['actual_demand']
    difference = abs(predicted_demand_int - actual_demand)
    percentage_error = (difference / actual_demand) * 100

    print(f"Date: {result['date']}")
    print(f"Predicted Demand: {predicted_demand_int} MWh")
    print(f"Actual Demand: {actual_demand} MWh")
    print(f"Difference: {difference} MWh")
    print(f"Percentage Error: {percentage_error:.2f}%")
    print("-" * 50)

import pickle
import xgboost as xgb
from flask import Flask, request, jsonify
import pandas as pd


model = xgb.Booster()
model.load_model("models/xgb_model.bin")
        
def prepare_data(new_data):
    new_observation = pd.DataFrame({
    'temperature' : [21],
    'year': [2024],
    'month': [8],
    'day': [12],
    'hr': [3],
    'day_of_week': [1],
    'is_weekend': [0],
    'holiday': [0]})
    return  new_observation 

def predict(features):
    features = xgb.DMatrix(features)
    predictions  = model.predict(features)
    return float(predictions[0])

app = Flask('Demand-prediction')



@app.route('/predict', methods=['POST'])
def predict_endpoint():
    ride = request.get_json()

    features = prepare_data(ride)
    pred = predict(features)

    result = {
        'duration': pred,
        'model_version': "2768ee8d9ae04948930e4d21b3d0ae57"
    }

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)
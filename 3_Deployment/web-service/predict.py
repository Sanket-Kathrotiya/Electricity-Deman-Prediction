import xgboost as xgb
from flask import Flask, request, jsonify
import pandas as pd


model = xgb.Booster()
model.load_model("xgb_model.bin")
        
def prepare_data(new_data):
    new_observation = pd.DataFrame([new_data])
    return  new_observation 

def predict(features):
    features = xgb.DMatrix(features)
    predictions  = model.predict(features)
    return float(predictions[0])

app = Flask('Demand-prediction')

@app.route('/predict', methods=['POST'])
def predict_endpoint():
    data = request.get_json()

    data = prepare_data(data)
    pred = predict(data)

    result = {
        'NYC electricity demand in megawatt-hours right now is ': pred,
    }

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)
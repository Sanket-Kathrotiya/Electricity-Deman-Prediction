import xgboost as xgb
from flask import Flask, request, jsonify
import pandas as pd


model = xgb.Booster()
model.load_model("xgb_model.bin")
        
def prepare_data(new_data):
    """
    Converts input data into a DataFrame.

    :param new_data: Input data to be converted into a DataFrame.
    :return: A DataFrame created from the input data.
    """
    new_observation = pd.DataFrame([new_data])
    return  new_observation 

def predict(features):
    """
    Makes a prediction using a pre-trained XGBoost model.

    :param features: Input features for making the prediction.
    :return: The first prediction value as a float.
    """
    features = xgb.DMatrix(features)
    predictions  = model.predict(features)
    return float(predictions[0])

app = Flask('Demand-prediction')

@app.route('/predict', methods=['POST'])
def predict_endpoint():
    """
    Handles a prediction request, prepares the input data, makes a prediction, and returns the result.

    :return: JSON response with the predicted NYC electricity demand in megawatt-hours.
    """

    data = request.get_json()

    data = prepare_data(data)
    pred = predict(data)

    result = {
        'NYC electricity demand in megawatt-hours right now is ': pred,
    }

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)
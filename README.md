# Electricity-Demand-Prediction

**This MLOps project focuses on predicting electricity demand in New York City using machine learning models.**

------------

## Project Overview

This MLOps project focuses on predicting electricity demand in New York City using machine learning models. The goal is to forecast electricity demand (in megawatt-hours) based on various factors such as time, weather conditions, and seasonal changes.

## Table of Contents

1. [Project Structure](#project-structure)
2. [Setup and Installation](#setup-and-installation)
3. [Data Collection and Preprocessing](#data-collection-and-preprocessing)
4. [Model Training](#model-training)
5. [Model Deployment](#model-deployment)
6. [Usage](#usage)
7. [Performance Metrics](#performance-metrics)
8. [Future Improvements](#future-improvements)

## Project Structure

The project consists of the following main components:

- `Dataset generation.ipynb`: Jupyter notebook for data collection and preprocessing
- `mlflow_experiments.ipynb`: Jupyter notebook for model experimentation using MLflow
- `orchestrate.py`: Main script for orchestrating the ML pipeline using Prefect
- `predict.py`: Flask application for serving predictions
- `test.py`: Script for testing the prediction endpoint

## Setup and Installation

1. Clone the repository:
   ```
   git clone https://github.com/your-username/Electricity-Demand-Prediction.git
   cd Electricity-Demand-Prediction
   ```

2. Create a virtual environment and install dependencies:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

3. Set up MLflow:
   ```
   mlflow server --backend-store-uri sqlite:///backend.db
   ```

## Data Collection and Preprocessing
The dataset includes historical electricity demand records, along with features such as date, time, temperature, and holidays. The data is processed to extract relevant time-based features like year, month, day, hour, day of the week, and whether it's a weekend or a holiday.

The project uses two main data sources:

1. Electricity demand data from the U.S. Energy Information Administration (EIA)
2. Temperature data from the Open-Meteo API

The `Dataset generation.ipynb` notebook handles the data collection and preprocessing steps:

- Fetching electricity demand data using the EIA API
- Retrieving historical temperature data for New York City
- Merging and preprocessing the datasets
- Feature engineering (extracting time-based features, adding holiday information)

## Model Training

The model training process is managed using MLflow and orchestrated with Prefect:

The `mlflow_experiments.ipynb` notebook is used for hyperparameter tuning. It explores different configurations to find the optimal set of hyperparameters for the XGBoost model.

After training, models are registered in the MLflow Model Registry. This allows for tracking models in different stages (such as staging and production), making it easier to manage model versions and transitions.

2. The `orchestrate.py` script defines the main training pipeline using Prefect tasks and flows:
   - Reading and preprocessing the dataset
   - Splitting the data into training and validation sets
   - Training an XGBoost model with hyperparameter tuning
   - Logging model parameters, metrics, and artifacts using MLflow

To run the training pipeline:

```
python orchestrate.py
```

## Model Deployment

The trained model is deployed as a Flask application in `predict.py`. This script:

- Loads the trained XGBoost model
- Defines a `/predict` endpoint that accepts POST requests with input features
- Returns predictions for electricity demand

To start the prediction service:

```
python predict.py
```

## Usage
### Local Deployment

To make a prediction, send a POST request to the `/predict` endpoint with the following JSON structure:

```json
{
    "temperature": 21,
    "year": 2024,
    "month": 8,
    "day": 12,
    "hr": 3,
    "day_of_week": 1,
    "is_weekend": 0,
    "holiday": 0
}
```

You can use the `test.py` script to test the prediction endpoint:

```
python test.py
```

### Docker Deployment

The model is also containerized using Docker for easy deployment and scalability. To build and run the Docker container:

1. Build the Docker image:
   ```
   docker build -t electricity-demand-prediction .
   ```

2. Run the container:
   ```
   docker run -p 9696:9696 electricity-demand-prediction
   ```

This exposes the prediction service on port 9696 of your local machine.

#### A Makefile is provided to automate common tasks in the project
Below are the available commands:
- `make setup`: Install the required dependencies.
- `make prefect-login`: Log in to Prefect Cloud.
- `make create-pool`: Create a Prefect work pool.
- `make schedule`: Schedule the workflow.
- `make orchestrate`: Run the Prefect orchestration.
- `make deploy`: Build and run the Docker container.
- `make test`: Run the test script to send prediction data.

## Performance Metrics

The model's performance is evaluated using the following metrics:

- Root Mean Squared Error (RMSE)
- R² Score

These metrics are logged and tracked using MLflow, allowing for easy comparison between different model versions and hyperparameter configurations.

Our best performing model achieved an RMSE of 377 MWh (megawatt-hours). Average demand of electricity in dataset is 17294 MWh. This indicates that, on average, our predictions deviate from the actual electricity demand by about 377 MWh. Given the scale of electricity consumption in a city like New York, this represents a strong predictive performance.

## Future Improvements

1. Incorporate additional features such as special events, economic indicators, or COVID-19 impact
2. Implement automated retraining to keep the model up-to-date with the latest data
3. Develop a user interface for easier interaction with the prediction service


Feel free to contribute to this project by opening issues or submitting pull requests!

import mlflow

import pandas as pd
from pandas.tseries.holiday import USFederalHolidayCalendar as calendar

import xgboost as xgb

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

from hyperopt import fmin, tpe, hp, STATUS_OK, Trials
from hyperopt.pyll import scope

import pathlib
from prefect import flow, task

@task(retries=3, retry_delay_seconds=2)
def read_dataframe(filename):
    """
    Reads a CSV file into a DataFrame, processes date and demand columns, and adds additional features.

    :param filename: Path to the CSV file to be read.
    :return: DataFrame with processed columns and additional features (year, month, day, hour, day_of_week, is_weekend, holiday).
    """
    df = pd.read_csv(filename)
    df['date'] = pd.to_datetime(df['date'])
    df['demand'] = pd.to_numeric(df['demand'], errors='coerce').astype('float')
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['hr'] = df['date'].dt.hour
    df['day_of_week'] = df['date'].dt.dayofweek  # Monday=0, Sunday=6
    df['is_weekend'] = df['date'].dt.dayofweek >= 5  # True if weekend, False otherwise
    
    holidays = calendar().holidays(start=df['date'].min(), end=df['date'].max())
    df['holiday'] = df['date'].isin(holidays).astype(int)
    
    return df

@task
def split_data(df):
    """
    Splits a DataFrame into training and validation sets for features and target.

    :param df: DataFrame containing the features and target variable. The 'demand' and 'date' columns are used to separate features from the target.
    :return: Tuple containing (X_train, X_val, y_train, y_val), where X_train and X_val are the feature sets, and y_train and y_val are the target sets.
    """
   
    X = df.drop('demand', axis=1)
    X = X.drop('date', axis=1)

    y = df['demand']
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
    return X_train, X_val, y_train, y_val

    
@task
def train_model(X_train, X_val, y_train, y_val):
    """
    Trains an XGBoost model and logs parameters and metrics using MLflow.

    :param X_train: Features for training the model.
    :param X_val: Features for validating the model.
    :param y_train: Target values for the training data.
    :param y_val: Target values for the validation data.

    :return: None. Saves the model and logs information to MLflow.
    """

    train = xgb.DMatrix(X_train, label=y_train)
    valid = xgb.DMatrix(X_val, label=y_val)

    best_params = ({'learning_rate': 0.18891478774394413,
                    'max_depth': 9, 
                    'min_child_weight': 6.642316776962908,
                    'reg_alpha': 0.012540977368792963, 
                    'reg_lambda': 0.012396118588604442})
    
    mlflow.log_params(best_params)
     
    model = xgb.train(
            params=best_params,
            dtrain=train,
            num_boost_round=2000,
            evals=[(valid, "validation")],
            early_stopping_rounds=20,
        )

    y_pred = model.predict(valid)
    rmse = mean_squared_error(y_val, y_pred, squared=False)
    mlflow.log_metric("rmse", rmse)
    
    pathlib.Path("models").mkdir(exist_ok=True)
    model.save_model("models/xgb_model.bin")   
    mlflow.xgboost.log_model(model, artifact_path="models_mlflow")
    
    return None

@flow(log_prints=True)
def main_flow(dataset_path):
    
    df = read_dataframe(dataset_path)
    
    mlflow.set_tracking_uri("http://127.0.0.1:5000") 
    mlflow.set_experiment("Electricity Demand Prediction")
    
    X_train, X_val, y_train, y_val = split_data(df)
    
    train_model(X_train, X_val, y_train, y_val)
    
    
if __name__ == "__main__":
    dataset_path = "1-Model_Training/mlflow/dataset.csv"
    main_flow(dataset_path )
    
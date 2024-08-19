import mlflow

import pandas as pd
from pandas.tseries.holiday import USFederalHolidayCalendar as calendar

import xgboost as xgb

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.linear_model import LinearRegression , Lasso
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor

from hyperopt import fmin, tpe, hp, STATUS_OK, Trials
from hyperopt.pyll import scope

import pathlib
from prefect import flow, task

@task(retries=3, retry_delay_seconds=2)
def read_dataframe(filename):
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
   
    X = df.drop('demand', axis=1)
    X = X.drop('date', axis=1)

    y = df['demand']
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
    return X_train, X_val, y_train, y_val
    
@task
def train_model(X_train, X_val, y_train, y_val):
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
    dataset_path = "1-Model_Training/Data/dataset.csv"
    main_flow(dataset_path)
    
### Electricity-Demand-Prediction

**This MLOps project focuses on predicting electricity demand in New York City using machine learning models.**

## Description:
Electricity demand in a bustling metropolis like New York City fluctuates significantly due to various factors such as time of day, weather conditions, and seasonal changes. The goal of this project is to build a predictive model that can accurately forecast the electricity demand (in megawatt-hours) for a given time, based on historical data and other relevant features.

## Data:
The dataset includes historical electricity demand records, along with features such as date, time, temperature, and holidays. The data is processed to extract relevant time-based features like year, month, day, hour, day of the week, and whether it's a weekend or a holiday.

## Key Objectives Achieved:

**Accurate Demand Forecasting:** Developed a robust machine learning model to predict electricity demand in New York City, enhancing grid management and resource allocation.
**Feature Engineering:** Utilized historical data to extract key features such as temperature, time of day, and holiday indicators, significantly improving model accuracy.
**Scalable MLOps Pipeline:**Implemented a scalable MLOps pipeline using Prefect and MLflow to automate data processing, model training, and deployment, ensuring efficient model management and updates.

# A Makefile is provided to automate common tasks in the project. Below are the available commands:
`make setup`: Install the required dependencies.
`make prefect-login`: Log in to Prefect Cloud.
`make create-pool`: Create a Prefect work pool.
`make schedule`: Schedule the workflow.
`make orchestrate`: Run the Prefect orchestration.
`make deploy`: Build and run the Docker container.
`make test`: Run the test script to send prediction data.

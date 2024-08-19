## Deployment

To deploy the model using Docker, follow these steps:
1. **Navigate to the Web Service Directory:**


```python
cd 3_Deployment/web-service
```
2. **Build the Docker Image:**
```python
docker build -t nyc-electricity-demand-prediction-service:v1 .
```
3. **Run the Docker Container:**
```python
docker run --rm -p 9696:9696 nyc-electricity-demand-prediction-service:v1 .
```

## Testing the Web Service

To test the web service and send data for prediction, follow these steps:
1. **Open a New Terminal**

Open a new terminal window or tab.

2. **Navigate to the Project Directory**
Change to the directory where the test.py script is located:
```python
cd 3_Deployment/web-service
```

3. **Run the Test Script**
Execute the test script using Python:
```python
python test.py
```

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
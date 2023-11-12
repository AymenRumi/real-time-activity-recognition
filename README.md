# Real Time Human Activity Recognition

## Project Overview
This `project` simulates a multidimensional stream of sensor data, using Apache Kafka for real-time data handling. It involves a Kafka producer pushing simulated sensor data in real-time, and a Kafka consumer classifying human activities from this data stream. The project uses Docker Compose to run the Kafka server and PyTorch for training a machine learning model. Model training experiments are tracked using MLFlow. The model is trained using a static dataset, windowed and loaded into PyTorch's DataLoader with a window size of 7. This trained model is then employed for real-time activity recognition.


## Demo

```bash
# Start zookeeper & kafka with docker-compose
docker-compose up 
```


```bash
# Run the stream data simulation
python -m src.jobs.start_stream
```


```bash
# Start the stream processing to recognize human activity (pytorch model must be trained)
python -m src.jobs.handle_stream
```


<img src="https://github.com/AymenRumi/real-time-activity-recognition/blob/main/assets/demo.gif">



## Getting Started
Prerequisites
<br />
Docker and Docker Compose
<br />
Python
<br />
Apache Kafka
<br />
PyTorch

## Training the Model
Load the static dataset.
Window the data with a size of 7.
Input the data into PyTorch's DataLoader.
Train the model using PyTorch.

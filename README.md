# Real Time Human Activity Recognition

## Project Overview
This project simulates a multidimensional stream of sensor data, using `Apache Kafka` for real-time data handling. It involves a Kafka producer pushing simulated sensor data in real-time, and a Kafka consumer classifying human activities from this data stream. The project uses `Docker Compose` to run the Kafka server and `PyTorch` for training a machine learning model. Model training experiments are tracked using `MLFlow`. The model is trained using a static dataset, windowed and loaded into PyTorch's `DataLoader` with a window size of 7. This trained model is then employed for real-time activity recognition.


## Project Demo

```bash
# Start zookeeper & kafka with docker-compose
docker-compose up 
```


```bash
# Run the stream data simulation script
python -m src.jobs.start_stream
```

```bash
# Start the stream handling script to recognize human activity (pytorch model must be trained)
python -m src.jobs.handle_stream
```


<img src="https://github.com/AymenRumi/real-time-activity-recognition/blob/main/assets/demo.gif">



## Getting Started
<b>Prerequisites</b>
<br />
Docker and Docker Compose
<br />
Python
<br />
Apache Kafka
<br />
PyTorch
<br />
MLFlow



```bash
# clone repo
git clone https://github.com/AymenRumi/real-time-activity-recognition.git
```

```bash
# start environment
python -m venv env
source env/bin/activate

pip install -r requirements.txt
```


## Training the Model

### Create Model Training Dataset

Dataset is chunked into instances of activity then windowed with a size of 7 (configurable) in directory struture for PyTorch's `DataLoader` class.

```bash
# Script for creating training data with, use flag -m to create with multithreads
python -m src.jobs.create_training_dataset -m
```
```bash
# Without multithreads (slower)
python -m src.jobs.create_training_dataset 

```


<img src="https://github.com/AymenRumi/real-time-activity-recognition/blob/main/assets/demo_dataset.gif">


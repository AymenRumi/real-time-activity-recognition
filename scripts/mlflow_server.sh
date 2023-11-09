#!/bin/bash


pid=$(lsof -t -i:5000)

# Check if the PID was found
if [ -z "$pid" ]
then
    echo "Port 5000 is free."
else
    kill -9 $pid
fi

mlflow server --backend-store-uri src/mlflow/mlflow_db --default-artifact-root ./src/mlflow/mlflowruns  --host 0.0.0.0  --port 5000
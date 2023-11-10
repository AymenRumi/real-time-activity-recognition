# Real time Human Activity Recognition

## TODO: Finnish Detailed ReadMe


### Demo

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


import json

import torch


def encode_sensor_data(data_point):
    return json.dumps(data_point).encode("utf-8")


def decode_sensor_data(stream_value):
    return json.loads(stream_value.decode("utf-8"))


def read_buffer(buffer: list):
    return torch.tensor([list(i.values()) for i in buffer])

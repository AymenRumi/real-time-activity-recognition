import pandas as pd


class HumanActivitySensor:
    def __init__(self):

        self.data_connection = None
        self.pointer = 0

    def __connect_to_source(self):
        self.data_connection = pd.read_df("../data/human_activity.csv")

    def start_sensor_stream(self):

        """
        while:
            push_to_topic



        """

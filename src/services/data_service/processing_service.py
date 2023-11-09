import os
from concurrent.futures import ThreadPoolExecutor

import pandas as pd

WINDOW_SIZE = 7
DATA_PATH = "src/data"


class DataWindowing:
    def __init__(self):
        self.create_folders()

    def create_folders(self, df: pd.DataFrame):
        for activity in df.activity.unique():

            new_path = f"{DATA_PATH}/{activity}"
            if not os.path.exists(new_path):

                os.makedirs(new_path)

    def label_activity_chunks(self, df: pd.DataFrame):
        chunk = 1
        chunk = [1] + [
            chunk := chunk + 1 if (activity != df["activity"][i + 1]) else chunk
            for i, activity in enumerate(df["activity"][:-1])
        ]
        return (
            df.assign(activity_chunk=chunk)
            .groupby(["activity", "activity_chunk"])
            .filter(lambda x: len(x) >= WINDOW_SIZE)
        )

    def process_chunk(self, df, activity_chunk):
        chunk = df.query("activity_chunk == @activity_chunk")
        if chunk.activity.nunique() == 1:
            folder = chunk.activity.unique()[0]
            [
                chunk[i : WINDOW_SIZE + i]
                .drop(columns=["activity", "activity_chunk"])
                .to_csv(
                    f"{DATA_PATH}/{folder}/chunk_{activity_chunk}_{i}.csv", index=False
                )
                for i in range(len(chunk) - WINDOW_SIZE + 1)
            ]

    def create_dataset_multithreaded(self, df: pd.DataFrame):

        activity_chunks = df.activity_chunk.unique()
        with ThreadPoolExecutor(max_workers=10) as executor:
            executor.map(lambda chunk: self.process_chunk(df, chunk), activity_chunks)

    def create_dataset(self, df: pd.DataFrame):

        for index, activity_chunk in enumerate(df.activity_chunk.unique()):
            chunk = df.query(f"activity_chunk == @activity_chunk")
            if chunk.activity.nunique() == 1:
                folder = chunk.activity.unique()[0]
                [
                    chunk[i : WINDOW_SIZE + i]
                    .drop(columns=["activity", "activity_chunk"])
                    .to_csv(
                        f"{DATA_PATH}/{folder}/chunk_{activity_chunk}_{i}.csv",
                        index=False,
                    )
                    for i in range(len(chunk) - WINDOW_SIZE + 1)
                ]

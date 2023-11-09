import os
from concurrent.futures import ThreadPoolExecutor

import pandas as pd

"""
Functions for creating dataset for model training, functions are called from jupyter notebook
"""

WINDOW_SIZE = 7
DATA_PATH = os.getcwd().replace("services", "data")


def create_folders(df: pd.DataFrame):
    for activity in df.activity.unique():

        new_path = f"{DATA_PATH}/{activity}"
        if not os.path.exists(new_path):

            os.makedirs(new_path)


def process_chunk(activity_chunk):
    chunk = df.query("activity_chunk == @activity_chunk")
    if chunk.activity.nunique() == 1:
        folder = chunk.activity.unique()[0]
        [
            chunk[i : WINDOW_SIZE + i]
            .drop(columns=["activity", "activity_chunk"])
            .to_csv(f"{DATA_PATH}/{folder}/chunk_{activity_chunk}_{i}.csv", index=False)
            for i in range(len(chunk) - WINDOW_SIZE + 1)
        ]


def create_dataset_multithreaded(df: pd.DataFrame):
    create_folders(df)

    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(process_chunk, df.activity_chunk.unique())


def create_dataset(df: pd.DataFrame):
    create_folders(df)

    for index, activity_chunk in enumerate(df.activity_chunk.unique()):
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

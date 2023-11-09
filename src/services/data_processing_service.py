import os
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

"""
Functions for creating dataset for model training, functions are called from jupyter notebook

"""

def create_folders(df:pd.DataFrame,, data_path:str):
    for activity in df.activity.unique():

        new_path = f"{data_path}/{activity}"
        if not os.path.exists(new_path):

            os.makedirs(new_path)


def process_chunk(activity_chunk, data_path):
    chunk = df.query(f"activity_chunk == {activity_chunk}")
    if chunk.activity.nunique() == 1:
        folder = chunk.activity.unique()[0]
        window_size = 7
        for i in range(len(chunk) - window_size + 1):
            chunk_slice = chunk[i : window_size + i].drop(
                columns=["activity", "activity_chunk"]
            )
            chunk_slice.to_csv(f"{data_path}/{folder}/chunk_{activity_chunk}_{i}.csv", index=False)
            print(f"saved to : {data_path}/{folder}/chunk_{activity_chunk}_{i}.csv")


def create_dataset_multithreaded(df:pd.DataFrame, data_path:str):
    create_folders(df)

    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(process_chunk, df.activity_chunk.unique())


def create_dataset(df:pd.DataFrame, data_path:str):

    create_folders(df)

    for index, activity_chunk in enumerate(df.activity_chunk.unique()):
        chunk = df.query("activity_chunk == @activity_chunk")
        window_size = 7
        if chunk.activity.nunique() == 1:
            folder = chunk.activity.unique()[0]
            for i in range(len(chunk) - window_size + 1):
                chunk[i : window_size + i].drop(columns=["activity", "activity_chunk"]).to_csv(f"{data_path}/{folder}/chunk_{activity_chunk}_{i}.csv", index=False)
                print(f"saved to : {data_path}/{folder}/chunk_{activity_chunk}_{i}.csv")

import click
import pandas as pd

from src.services.data_service import (
    create_dataset,
    create_dataset_multithreaded,
    create_folders,
    label_activity_chunks,
)
from src.utils.logging import logger

DATA_PATH = "src/data/train.csv"


@click.command()
@click.option("-m", "--multithreaded", is_flag=True, help="Run in multithreaded mode.")
def run(multithreaded):
    df = pd.read_csv(DATA_PATH).pipe(label_activity_chunks).drop(columns=["rn"])
    create_folders(df)

    if multithreaded:
        logger.task("Creating training data: executing with multithreads")
        create_dataset_multithreaded(df)
    else:
        logger.task("Creating training data")
        create_dataset(df)


if __name__ == "__main__":
    run()

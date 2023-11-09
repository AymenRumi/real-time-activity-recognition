import sys
from pathlib import Path

import click
import pandas as pd

scripts_dir = Path(__file__).parent.absolute()
parent_dir = scripts_dir.parent
sys.path.append(str(parent_dir))


from src.services.data_processing_service import (
    create_dataset,
    create_dataset_multithreaded,
    label_activity_chunks,
)
from src.utils.logging import logger

DATA_PATH = "src/data/train.csv"


@click.command()
@click.option("-m", "--multithreaded", is_flag=True, help="Run in multithreaded mode.")
def run(multithreaded):
    df = pd.read_csv(DATA_PATH).pipe(label_activity_chunks)
    if multithreaded:
        logger.task("Creating training data: executing with multithreads")
        create_dataset_multithreaded(df)
    else:
        logger.task("Creating training data")
        create_dataset(df)


if __name__ == "__main__":
    run()

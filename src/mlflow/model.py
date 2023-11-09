import click
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

import mlflow


@click.command(help="This program trains a random forest model.")
@click.option(
    "--data_file",
    default="data/train.csv",
    help="Path to the CSV file containing the training data.",
)
@click.option(
    "--model_output", default="model", help="Path to output the trained model file."
)
def train_model(data_file, model_output):
    # Read in the data
    data = pd.read_csv(data_file)
    y = data.pop("target")
    X = data

    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y)

    # Train the model
    with mlflow.start_run():
        model = RandomForestClassifier()
        model.fit(X_train, y_train)

        # Evaluate the model
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)

        # Log the model
        mlflow.log_param("accuracy", accuracy)
        mlflow.sklearn.log_model(model, model_output)


if __name__ == "__main__":
    train_model()  # pylint: disable=no-value-for-parameter

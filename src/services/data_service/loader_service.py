import os

import pandas as pd
import torch
from torch.utils.data import DataLoader, Dataset

from src.constants import label_mapping

DIRECTORY_PATH = "src/data"


class CustomDataset(Dataset):
    def __init__(self, directory):
        self.data_files = []
        self.labels = []

        for label_folder in os.listdir(directory):
            label_path = os.path.join(directory, label_folder)
            if os.path.isdir(label_path):

                label = label_mapping[label_folder]
                for file in os.listdir(label_path):
                    if file.endswith(".csv"):
                        file_path = os.path.join(label_path, file)
                        self.data_files.append(file_path)
                        self.labels.append(label)

    def __len__(self):
        return len(self.data_files)

    def __getitem__(self, idx):

        data_array = pd.read_csv(self.data_files[idx]).to_numpy().reshape(1, 7, 561)
        label = self.labels[idx]
        return torch.tensor(data_array, dtype=torch.float32), label


def create_data_loaders(directory=DIRECTORY_PATH, batch_size=32, train_split=0.8):
    # Create the full dataset
    full_dataset = CustomDataset(directory)

    # Splitting the dataset
    total_size = len(full_dataset)
    train_size = int(train_split * total_size)
    test_size = total_size - train_size
    train_dataset, test_dataset = torch.utils.data.random_split(
        full_dataset, [train_size, test_size]
    )

    # Create DataLoaders for both datasets
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=True)

    return train_loader, test_loader

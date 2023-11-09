import os

import pandas as pd
import torch
from torch.utils.data import DataLoader, Dataset


class CustomDataset(Dataset):
    def __init__(self, directory):
        self.data_files = []
        self.labels = []

        # Define a mapping for the labels
        self.label_mapping = {
            "LAYING": 0,
            "SITTING": 1,
            "STANDING": 2,
            "WALKING": 3,
            "WALKING_DOWNSTAIRS": 4,
            "WALKING_UPSTAIRS": 5,
        }

        # Scanning through the directory and subdirectories
        for label_folder in os.listdir(directory):
            label_path = os.path.join(directory, label_folder)
            if os.path.isdir(label_path):
                # Extract label from folder name
                label = self.label_mapping[label_folder]
                for file in os.listdir(label_path):
                    if file.endswith(".csv"):
                        file_path = os.path.join(label_path, file)
                        self.data_files.append(file_path)
                        self.labels.append(label)

    def __len__(self):
        return len(self.data_files)

    def __getitem__(self, idx):
        # Read the CSV file and convert to numpy array
        data_array = pd.read_csv(self.data_files[idx]).to_numpy()
        label = self.labels[idx]
        return torch.tensor(data_array, dtype=torch.float32), label


def create_data_loader(directory, batch_size=32, shuffle=True):
    dataset = CustomDataset(directory)
    return DataLoader(dataset, batch_size=batch_size, shuffle=shuffle)


# Example usage
data_loader = create_data_loader("src/data/HAR", batch_size=64)

# # In your training loop
# for data, labels in data_loader:
#     # Use data and labels for training
#     pass

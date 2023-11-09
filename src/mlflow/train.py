import torch
import torch.nn as nn
from tqdm import tqdm

from src.mlflow.model import ConvNN
from src.services.data_service import create_data_loaders

if __name__ == "__main__":
    model = ConvNN()

    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

    train_data_loader, test_data_loader = create_data_loaders()
    num_epochs = 10
    print("training")
    for epoch in tqdm(range(num_epochs)):

        for i, (images, labels) in enumerate(
            train_data_loader
        ):  # Assuming you have a data_loader
            # Forward pass
            print(images.size())
            outputs = model(images)
            loss = criterion(outputs, labels)

            # Backward and optimize
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            if (i + 1) % 20 == 0:
                print(
                    f"Epoch [{epoch+1}/{num_epochs}], Step [{i+1}/{len(train_data_loader)}], Loss: {loss.item():.4f}"
                )

    # torch.save({
    #     'model_state_dict': model.state_dict(),
    #     'optimizer_state_dict': optimizer.state_dict(),
    #     'loss': loss,
    # }, f'checkpoint.pth')

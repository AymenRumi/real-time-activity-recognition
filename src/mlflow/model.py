import torch.nn as nn
import torch.nn.functional as F


class ConvNN(nn.Module):
    def __init__(self, num_classes=6):
        super(ConvNN, self).__init__()

        # Convolutional layers
        self.conv1 = nn.Conv2d(1, 32, 3, stride=1, padding=1)
        self.conv2 = nn.Conv2d(32, 64, 3, stride=1, padding=1)

        # Pooling layer
        self.pool = nn.MaxPool2d(2, 2)

        def conv2d_size_out(size, kernel_size=3, stride=1, padding=1):
            return (size + 2 * padding - (kernel_size - 1) - 1) // stride + 1

        def pool_size_out(size, kernel_size=2, stride=2):
            return (size - (kernel_size - 1) - 1) // stride + 1

        convw = conv2d_size_out(conv2d_size_out(561))
        convh = conv2d_size_out(conv2d_size_out(7))
        poolw = pool_size_out(pool_size_out(convw))
        poolh = pool_size_out(pool_size_out(convh))

        linear_input_size = poolw * poolh * 64

        self.fc1 = nn.Linear(linear_input_size, 1000)
        self.fc2 = nn.Linear(1000, num_classes)

    def forward(self, x):

        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))

        # Flatten the output for the fully connected layer
        x = x.view(-1, self.num_flat_features(x))

        # Apply fully connected layers with ReLU and output layer
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x

    def num_flat_features(self, x):
        size = x.size()[1:]
        num_features = 1
        for s in size:
            num_features *= s
        return num_features

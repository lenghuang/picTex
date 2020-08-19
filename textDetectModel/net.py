import torch.nn as nn
import torch.nn.functional as F
from classes import classes


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv11 = nn.Conv2d(in_channels=1, out_channels=20,
                                kernel_size=5, padding=2)
        self.conv12 = nn.Conv2d(20, 20, 5, padding=2)
        self.batch1 = nn.BatchNorm2d(20)
        self.pool1 = nn.MaxPool2d(kernel_size=2, stride=2)
        self.conv21 = nn.Conv2d(20, 40, 5, padding=2)
        self.conv22 = nn.Conv2d(40, 40, 5, padding=2)
        self.batch2 = nn.BatchNorm2d(40)
        self.pool2 = nn.MaxPool2d(2, 2)

        # Transitioning from Conv ===> Linear
        # 16 is the number of output channels in the previous conv layer.

        self.fc1 = nn.Linear(40 * 8 * 8, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, len(classes))
        self.drop = nn.Dropout(0.5)
        self.soft = nn.Softmax(dim=1)

    def forward(self, x):
        x = F.relu(self.conv11(x))
        x = F.relu(self.conv12(x))
        x = self.batch1(x)
        x = self.pool1(x)
        x = F.relu(self.conv21(x))
        x = F.relu(self.conv22(x))
        x = self.batch2(x)
        x = self.pool2(x)
        x = x.view(-1, 40 * 8 * 8)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        x = self.drop(x)
        x = self.soft(x)
        return x

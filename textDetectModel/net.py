import torch.nn as nn
import torch.nn.init as init

from classes import classes


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.relu = nn.ReLU(inplace=False)
        self.conv11 = nn.Conv2d(in_channels=1,
                                out_channels=10, kernel_size=5, padding=2)
        self.conv12 = nn.Conv2d(10, 10, 5, padding=2)
        self.batch1 = nn.BatchNorm2d(10)
        self.pool1 = nn.MaxPool2d(kernel_size=2, stride=2)
        self.conv21 = nn.Conv2d(10, 20, 5, padding=2)
        self.conv22 = nn.Conv2d(20, 20, 5, padding=2)
        self.batch2 = nn.BatchNorm2d(20)
        self.pool2 = nn.MaxPool2d(2, 2)
        self.conv31 = nn.Conv2d(20, 40, 5, padding=2)
        self.conv32 = nn.Conv2d(40, 40, 5, padding=2)
        self.batch3 = nn.BatchNorm2d(40)
        self.pool3 = nn.MaxPool2d(2, 2)

        # Transitioning from Conv ===> Linear
        # 16 is the number of output channels in the previous conv layer.

        self.fc1 = nn.Linear(40 * 4 * 4, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, len(classes))
        self.dropconv = nn.Dropout(0.2)
        self.dropfc = nn.Dropout(0.4)
        self.soft = nn.Softmax(dim=1)

    def forward(self, x):
        x = self.relu(self.conv11(x))
        x = self.relu(self.conv12(x))
        x = self.batch1(x)
        x = self.pool1(x)
        x = self.relu(self.conv21(x))
        x = self.relu(self.conv22(x))
        x = self.batch2(x)
        x = self.pool2(x)
        x = self.relu(self.conv31(x))
        x = self.relu(self.conv32(x))
        x = self.batch3(x)
        x = self.pool3(x)
        x = x.view(-1, 40 * 4 * 4)
        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))
        x = self.fc3(x)
        x = self.dropfc(x)
        x = self.soft(x)
        return x
    def _initialize_weights(self):
        init.orthogonal_(self.conv11.weight, init.calculate_gain('relu'))
        init.orthogonal_(self.conv12.weight, init.calculate_gain('relu'))

        init.orthogonal_(self.conv21.weight, init.calculate_gain('relu'))
        init.orthogonal_(self.conv22.weight, init.calculate_gain('relu'))

        init.orthogonal_(self.conv31.weight, init.calculate_gain('relu'))
        init.orthogonal_(self.conv32.weight, init.calculate_gain('relu'))

        init.orthogonal_(self.fc1, init.calculate_gain('relu'))
        init.orthogonal_(self.fc2, init.calculate_gain('relu'))
        init.orthogonal_(self.fc3)






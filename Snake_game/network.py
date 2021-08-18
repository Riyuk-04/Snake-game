import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms

Max_Size = 50

class Net(nn.Module):

    def __init__(self):
        super(Net, self).__init__()
        # 1 input image channel, 6 output channels, 3x3 square convolution
        # kernel
        self.conv1 = nn.Conv2d(1, 6, 2)
        self.conv2 = nn.Conv2d(6, 10, 2)
        # an affine operation: y = Wx + b
        self.fc1 = nn.Linear(10 * 100 * 2, 120)  # 5*5 from image dimension
        self.fc2 = nn.Linear(120, 50)
        self.fc3 = nn.Linear(50, 4)

    def forward(self, x):
        # Max pooling over a (2, 2) window
        x = F.relu(self.conv1(x))
        # If the size is a square you can only specify a single number
        x = F.relu(self.conv2(x))
        x = x.view(-1, self.num_flat_features(x))
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return F.softmax(x)

    def num_flat_features(self, x):
        size = x.size()[1:]  # all dimensions except the batch dimension
        num_features = 1
        for s in size:
            num_features *= s
        return num_features

for x in range(10):
  for i, (input,target) in enumerate(dl_train):
    input, target = input.to(device), target.to(device)
    output = net(input)
   # print(target)

    optimizer.zero_grad()
    loss = criterion(output, target)
    loss.backward()
    optimizer.step()
  print(loss)

correct = 0
total = 0
with torch.no_grad():
  for i, (input,target) in enumerate(dl_test):
    input, target = input.to(device), target.to(device)
    output = net(input)
    _, pred = torch.max(output.data,1)
    total += target.size(0)
    correct += (pred == target).sum().item()
print(correct/total)
from sklearn.metrics import confusion_matrix
import torch
import torchvision.transforms as transforms
import torchvision.datasets as datasets
import torchvision.models as models
import torch.nn as nn
import torch.optim as optim
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import torch.nn.functional as F
import os 


transformations = transforms.Compose([
    transforms.Resize(255),
    transforms.CenterCrop(224),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(20,resample= Image.BILINEAR),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

train_set = datasets.ImageFolder(r"/Users/jonathanmairena/Documents/Fall2020/SeniorDesign/OtoscopeImages/Training", transform = transformations)

test_set = datasets.ImageFolder(r"/Users/jonathanmairena/Documents/Fall2020/SeniorDesign/OtoscopeImages/Testing", transform = transformations)

train_loader = torch.utils.data.DataLoader(train_set, batch_size=300, shuffle=True)
test_loader = torch.utils.data.DataLoader(test_set, batch_size=20, shuffle=True)

trainimages, trainlabels = next(iter(train_loader))
testimages, testlabels = next(iter(test_loader))


device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
num_epochs = 5
num_classes = 4
batch_size = 20
learning_rate = 0.001

class CNN(nn.Module): 
    def __init__(self):
        super(CNN, self).__init__()
        self.conv1 = nn.Conv2d(in_channels=3, out_channels=10, kernel_size=3)
        self.conv2 = nn.Conv2d(10, 20, kernel_size=3)
        self.conv2_drop = nn.Dropout2d() 
        self.fc1 = nn.Linear(58320, 512) # change first input based on hyperparameters
        self.fc2 = nn.Linear(512, 16)
        self.fc3 = nn.Linear(16,2)
        self.soft = nn.Softmax(dim = 1)

    def forward(self, x):
        x = F.relu(F.max_pool2d(self.conv1(x), 2))
        x = F.relu(F.max_pool2d(self.conv2_drop(self.conv2(x)), 2))
        x = x.view(x.shape[0],-1)
        x = F.relu(self.fc1(x))
        x = F.dropout(x, training=self.training)
        x = self.fc2(x)
        x = self.fc3(F.relu(x))
        x = self.soft(x)
        return x
    
    
    
# Initialize the prediction and label lists(tensors)
predlist=torch.zeros(0,dtype=torch.long, device='cpu')
lbllist=torch.zeros(0,dtype=torch.long, device='cpu')


model = CNN().to(device)
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(),lr = learning_rate)

# keeping-track-of-losses 
train_losses = []
valid_losses = []

for epoch in range(1, num_epochs + 1):
    # keep-track-of-training-and-validation-loss
    train_loss = 0.0
    valid_loss = 0.0
    correct_train = 0
    correct_test = 0
    total_train = 0
    total_test = 0
    # training-the-model
    model.train()
    for data, target in train_loader:
        # move-tensors-to-GPU 
        data = data.to(device)
        target = target.to(device)
        
        # clear-the-gradients-of-all-optimized-variables
        optimizer.zero_grad()
        # forward-pass: compute-predicted-outputs-by-passing-inputs-to-the-model
        output = model(data)
        # calculate-the-batch-loss
        loss = criterion(output, target)
        # backward-pass: compute-gradient-of-the-loss-wrt-model-parameters
        loss.backward()
        # perform-a-ingle-optimization-step (parameter-update)
        optimizer.step()
        # update-training-loss
        train_loss += loss.item() * data.size(0)
        
        #Accuracy 
        _, predicted = torch.max(output.data, 1)
        total_train += target.nelement()
        correct_train += predicted.eq(target.data).sum().item()
        train_accuracy = 100 * correct_train / total_train
        
    # validate-the-model
    model.eval()
    for data, target in test_loader:
        
        data = data.to(device)
        target = target.to(device)
        
        output = model(data)
        
        loss = criterion(output, target)
        
        # update-average-validation-loss 
        valid_loss += loss.item() * data.size(0)
        
        #Accuracy 
        _, predicted = torch.max(output.data, 1)
        total_test += target.nelement()
        correct_test += predicted.eq(target.data).sum().item()
        test_accuracy = 100 * correct_test / total_test
        
        #Confusion Matrix
        predlist=torch.cat([predlist,predicted.view(-1).cpu()])
        lbllist=torch.cat([lbllist,target.view(-1).cpu()])       
            

    # calculate-average-losses
    train_loss = train_loss/len(train_loader.sampler)
    valid_loss = valid_loss/len(test_loader.sampler)
    train_losses.append(train_loss)
    valid_losses.append(valid_loss)
        
    # print-training/validation-statistics 
    print('Epoch: {} \tTraining Loss: {:.6f} \tValidation Loss: {:.6f} \tTrain Accuracy: {:.6f} \tTest Accuracy: {:.6f}'.format(epoch, train_loss, valid_loss, train_accuracy, test_accuracy) )

conf_mat=confusion_matrix(lbllist.numpy(), predlist.numpy())
print(conf_mat)

    #print('Epoch: {} \tTraining Loss: {:.6f}'.format(
    #    epoch, train_loss))
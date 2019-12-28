import sklearn.datasets
import torch
import numpy as np
from numpy import loadtxt

labels = ["No event", "Earthquake"]
data = loadtxt('./vectors/data_training.csv', delimiter=',')
dataLabels = loadtxt('./vectors/data_training_ans.csv', delimiter=',')

np.random.seed(0)
X, y = data, dataLabels


import matplotlib.pyplot as plt

plt.scatter(X[:,0],X[:,1],s=40,c=y,cmap=plt.cm.binary)


X = torch.from_numpy(X).type(torch.FloatTensor)
y = torch.from_numpy(y).type(torch.LongTensor)


import torch.nn as nn
import torch.nn.functional as F

#our class must extend nn.Module
class Net(nn.Module):
    def __init__(self):
        super(Net,self).__init__()
        #Our network consists of 3 layers. 1 input, 1 hidden and 1 output layer
        #This applies Linear transformation to input data. 
        self.fc1 = nn.Linear(36,4)
        
        #This applies linear transformation to produce output data
        self.fc2 = nn.Linear(4,2)
        
    #This must be implemented
    def forward(self,x):
        #Output of the first layer
        x = self.fc1(x)
        #Activation function is Relu. Feel free to experiment with this
        x = torch.tanh(x)
        #This produces output
        x = self.fc2(x)
        return x
        
    #This function takes an input and predicts the class, (0 or 1)        
    def predict(self,x):
        #Apply softmax to output
        pred = F.softmax(self.forward(x), dim=0)
        ans = []
        for t in pred:
            if t[0]>t[1]:
                ans.append(0)
            else:
                ans.append(1)
        return torch.tensor(ans)
        

#Initialize the model        
model = Net()
#Define loss criterion
criterion = nn.CrossEntropyLoss()
#Define the optimizer
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

#Number of epochs
epochs = 4
#List to store losses
losses = []
for i in range(epochs):
    print(i+1)
    #Precit the output for Given input
    y_pred = model.forward(X)
    #Compute Cross entropy loss
    loss = criterion(y_pred,y)
    #Add loss to the list
    losses.append(loss.item())
    #Clear the previous gradients
    optimizer.zero_grad()
    #Compute gradients
    loss.backward()
    #Adjust weights
    optimizer.step()
    

from sklearn.metrics import accuracy_score
print(accuracy_score(model.predict(X),y))
    

def predict(x):
    x = torch.from_numpy(x).type(torch.FloatTensor)
    ans = model.predict(x)
    return ans.numpy()

test_x = loadtxt('./vectors/data_test.csv', delimiter=',')
testLabels = loadtxt('./vectors/data_test_ans.csv', delimiter=',')
predictions = predict(test_x)

for i in range(len(test_x)):
    print("Label:",testLabels[i], "Prediction:", predictions[i])





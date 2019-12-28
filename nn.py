import torch
import numpy as np
from torch.autograd import Variable
from torch.nn import Linear, ReLU, CrossEntropyLoss, Sequential
from torch.optim import Adam
from sklearn.model_selection import train_test_split
# load numpy array from csv file
from numpy import loadtxt
# load array

label = ["Sin evento", "Terremoto", "Otro"]
data = loadtxt('data.csv', delimiter=',')
data2 = loadtxt('data2.csv', delimiter=',')

# print the array
data = np.array([data])
data2 = np.array([data2])

print(data.shape)
print(data2.shape)
# data = np.delete(data, slice(779, 802), 1)

data = np.concatenate((data,data2))

train_x = np.array(data) #dataset with the Delta Vectors
print(train_x.shape)
train_y = np.array([0,0]) #labels for the dataset

train_x, val_x, train_y, val_y = train_test_split(train_x, train_y, test_size = 0.1, stratify = train_y)
# number of neurons in each layer
input_num_units = 780
hidden_num_units = 500
output_num_units = 2

# set remaining variables
epochs = 20
learning_rate = 0.0005

# define model
model = Sequential(Linear(input_num_units, hidden_num_units),
                   ReLU(),
                   Linear(hidden_num_units, output_num_units))
# loss function
loss_fn = CrossEntropyLoss()

# define optimization algorithm
optimizer = Adam(model.parameters(), lr=learning_rate)

train_losses = []
val_losses = []
for epoch in range(epochs):
    avg_cost = 0
    
    x, y = Variable(torch.from_numpy(train_x)), Variable(torch.from_numpy(train_y), requires_grad=False)
    x_val, y_val = Variable(torch.from_numpy(val_x)), Variable(torch.from_numpy(val_y), requires_grad=False)
    pred = model(x.float())
    pred_val = model(x_val.float())

    # get loss
    loss = loss_fn(pred, y)
    loss_val = loss_fn(pred_val, y_val)
    train_losses.append(loss)
    val_losses.append(loss_val)

    # perform backpropagation
    loss.backward()
    optimizer.step()
    avg_cost = avg_cost + loss.data

    if (epoch%2 != 0):
        print(epoch+1, avg_cost)
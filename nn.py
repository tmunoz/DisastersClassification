import torch
import numpy as np
from torch.autograd import Variable
from torch.nn import Linear, ReLU, CrossEntropyLoss, Sequential
from torch.optim import Adam
from sklearn.model_selection import train_test_split
# load numpy array from csv file
from numpy import loadtxt
# load array

labels = ["No event", "Earthquake", "Other"]
data = loadtxt('./vectors/data_training.csv', delimiter=',')
dataLabels = loadtxt('./vectors/data_training_ans.csv', delimiter=',')

train_x = np.array(data) #dataset with the Delta Vectors || Think that I shouldn't be calling np.array as data is already a np.array
print(train_x.shape)
train_y = np.array([1, 1, 0, 0, 0, 0, 0, 0]) #labels for the dataset || same that line 15
print(train_y.shape)
train_x, val_x, train_y, val_y = train_test_split(train_x, train_y, test_size = 0.5, stratify = train_y)
# number of neurons in each layer
input_num_units = 36
hidden_num_units = 500
output_num_units = 2

# set remaining variables
epochs = 100
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

test_x = loadtxt('./vectors/data_test.csv', delimiter=',')
predictions = np.argmax(model(torch.from_numpy(test_x).float()).data.numpy(), axis=1)

print(predictions)
for i in range(len(predictions)):
    print(test_x[i], predictions[i])

from numpy import loadtxt
import numpy as np
# load array

labels = ["No event", "Earthquake", "Other"]
data = loadtxt('vectors/data_training.csv', delimiter=',')
print(data.shape)
print(data)
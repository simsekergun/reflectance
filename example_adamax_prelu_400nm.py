# -*- coding: utf-8 -*-
"""Example_Adamax_Prelu_400nm

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1YNWtT8V4w6GQAsSFlVJvSfM5Gg2e8rm0
"""

!pip install -q keras
import tensorflow as tf
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt
import pandas
from numpy import zeros, newaxis
from __future__ import absolute_import, division, print_function

# load training data, p-polarization laser, silicon substrate
df = pandas.read_csv('trainSiP.csv', header=None)
# load training data, s-polarization laser, silicon substrate
df2 = pandas.read_csv('trainSiS.csv', header=None)
# load training data, p-polarization laser, glass substrate
df3 = pandas.read_csv('trainGlP.csv', header=None)
# load training data, s-polarization laser, glass substrate
df4 = pandas.read_csv('trainGlS.csv', header=None)
train_lines = np.dstack((df.values,df2.values,df3.values,df4.values))
train_labels = np.arange(3060)
# load experimental data, p-polarization laser, silicon substrate
df1 = pandas.read_csv('testSiP.csv', header=None)
# load experimental data, s-polarization laser, silicon substrate
df2 = pandas.read_csv('testSiS.csv', header=None)
# load experimental data, p-polarization laser, glass substrate
df3 = pandas.read_csv('testGlP.csv', header=None)
# load experimental data, s-polarization laser, glass substrate
df4 = pandas.read_csv('testGlS.csv', header=None)
test_line =  np.column_stack((df1.values,df2.values,df3.values,df4.values))

from keras.layers.advanced_activations import LeakyReLU, PReLU
from tensorflow.keras import layers
model = keras.Sequential()
model.add(keras.layers.Flatten(input_shape=(61,4)))
model.add(keras.layers.Dense(3060))
model.add(layers.PReLU(alpha_initializer='zeros', alpha_regularizer=None, alpha_constraint=None, shared_axes=None))
model.add(keras.layers.Dense(3060, activation='softmax'))

model.compile(optimizer='Adamax', 
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

counter = 0
losses = np.array(0.0)
accura = np.array(0.0)
nrs = np.array(0.0)
nis = np.array(0.0)
while counter<601:  
  history = model.fit(train_lines, train_labels, epochs=1, verbose=0)
  losss = history.history['loss']
  los = float(losss[0])
  accc = history.history['acc']
  accu = float(accc[0])
    
  losses = np.append(losses,los)
  accura = np.append(accura,accu)
  predictions = model.predict(test_line[newaxis,:, :])
  indd = np.argsort(predictions)
  wvals = predictions[0,indd[0,-4:]]
  
  rvals = (np.floor_divide(indd[0,-4:],51)+1)/10
  ivals = (np.remainder(indd[0,-4:],51))/10
  nr = np.sum(wvals*rvals)/np.sum(wvals)
  ni = np.sum(wvals*ivals)/np.sum(wvals)
  
  print(counter, "{:.3f}".format(los),"{:.3f}".format(accu),"{:.3f}".format(nr),"{:.3f}".format(ni))
  big_values = predictions[predictions>np.amax(predictions)/100]
  if accu>0.5:
    nrs = np.append(nrs,nr)
    nis = np.append(nis,ni)
  counter = counter + 1

np.savetxt('adamax_prelu_400_losses.csv', [losses[1:]], delimiter=',')
np.savetxt('adamax_prelu_400_accura.csv', [accura[1:]], delimiter=',')

predictions = model.predict(test_line[newaxis,:, :])
plt.figure(figsize=(16,9))
plt.plot(predictions.T)
plt.show()

# TRUE ANSWER IS
# 400   2.5051e+00 + 3.7393e+00i




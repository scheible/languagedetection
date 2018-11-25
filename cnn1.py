# -*- coding: utf-8 -*-
"""
Created on Sun Nov 25 18:12:01 2018

@author:qiany
"""

import numpy as np
import keras
import matplotlib.pyplot as plt
import random

#import data
from input_para import input_from
(x_train, y_train),(x_test,y_test) = input_from("Arabic")

#decide model
from keras import layers
from keras import models

model = models.Sequential()

#three convolutional layers
model.add(layers.Conv2D(32,(3,3),activation='relu',input_shape =(40,430,1)))
model.add(layers.MaxPooling2D(2,2))
model.add(layers.Conv2D(32,(3,3),activation='relu'))
model.add(layers.MaxPooling2D(2,2))
model.add(layers.Conv2D(64,(3,3),activation='relu'))

#model.summary()

#convert 3D to 1D
model.add(layers.Flatten())
#fully-connected layer
model.add(layers.Dense(64,activation='relu'))
model.add(layers.Dense(10,activation='softmax'))

#reshape data,scalling into [0,1]
train_images = x_train.reshape((x_train.shape[0],40,430,1))
train_images = x_train.astype('float32')/255
test_images = x_test.reshape((x_test.shape[0],40,430,1))
test_images = test_images.astype('float32')/255

#categorically encode the labels
from keras.utils import to_categorical
#Converts a class vector (integers) to binary class matrix
train_labels = to_categorical(y_train)
test_labels = to_categorical(y_test)

#Before training a model, you need to configure the learning process,
model.compile(optimizer='rmsprop',
              loss='categorical_crossentropy',
              metrics=['accuracy'])
# For a multi-class classification problem

#training use fit
model.fit(train_images,train_labels,epochs=5, batch_size=128)

#evaluate
test_loss, test_acc = model.evaluate(test_images,test_labels)
print(test_acc)
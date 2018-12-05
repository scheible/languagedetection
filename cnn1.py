#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 25 18:12:01 2018

@author:qiany
"""
from keras import layers
from keras import models
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.utils import to_categorical
from input_para import input_from
import numpy as np
import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt


def load():
    try:
        x_train = np.load("train_mfccs.npy")
        x_val = np.load("validation_mfccs.npy")
        x_test = np.load("test_mfccs.npy")
        y_train = np.load("train_labels.npy")
        y_val = np.load("validation_labels.npy")
        y_test = np.load("test_labels.npy")
    except(IOError):
        return None

    return (x_train, y_train), (x_val, y_val), (x_test, y_test)


def save(x_train, y_train, x_test, y_test, x_val, y_val):
    # save the mfccs
    np.save("train_mfccs.npy", x_train)
    np.save("test_mfccs.npy", x_test)
    np.save("train_labels.npy", y_train)
    np.save("test_labels.npy", y_test)
    np.save("validation_mfccs.npy", x_val)
    np.save("validation_labels.npy", y_val)


def main():
    # import data
    loaded = load()
    if loaded is None:
        (x_train, y_train), (x_val, y_val), (x_test, y_test) = input_from("subset")
        save(x_train, y_train, x_test, y_test, x_val, y_val)
    else:
        (x_train, y_train), (x_val, y_val), (x_test, y_test) = loaded

    # decide model
    model = models.Sequential()

    # three convolutional layers
    model.add(layers.Conv2D(32, (3, 3), activation='relu',
                            input_shape=(40, 430, 1)))
    model.add(layers.MaxPooling2D(2, 2))
    model.add(layers.Conv2D(32, (3, 3), activation='relu'))
    model.add(layers.MaxPooling2D(2, 2))
    model.add(layers.Conv2D(64, (3, 3), activation='relu'))

    # model.summary()

    # convert 3D to 1D
    model.add(layers.Flatten())
    # fully-connected layer
    model.add(layers.Dense(64, activation='relu'))
    model.add(layers.Dropout(0.5))
    model.add(layers.Dense(5, activation='softmax'))

    # reshape data, scalling into [0, 1]
    train_images = x_train.reshape((x_train.shape[0], 40, 430, 1))
    train_images = train_images.astype('float32')/255
    test_images = x_test.reshape((x_test.shape[0], 40, 430, 1))
    test_images = test_images.astype('float32')/255

    # categorically encode the labels
    # Converts a class vector (integers) to binary class matrix
    train_labels = to_categorical(y_train)
    test_labels = to_categorical(y_test)

    # Before training a model, you need to configure the learning process,
    model.compile(optimizer='rmsprop',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])
    model.summary()
    # For a multi-class classification problem

    cb = EarlyStopping(patience=3)

    # training use fit
    history = model.fit(train_images, train_labels, epochs=20,  batch_size=64,
                        validation_data=(x_val, y_val), callbacks=[])
    plt.plot(history.history['acc'])
    plt.plot(history.history['val_acc'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'validation'], loc='upper left')
    plt.savefig("accuracy_dropout.png")

    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'validation'], loc='upper left')
    plt.savefig("loss_dropout.png")

    # evaluate
    test_loss, test_acc = model.evaluate(test_images, test_labels)
    print(test_acc)


if __name__ == '__main__':
    main()

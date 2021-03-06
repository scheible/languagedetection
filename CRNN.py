#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Copyright © 2018 Gianmarco Garrisi
# Copyright © 2018 Qianyun Hu
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 3
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.

from keras import layers
from keras import models
from keras.callbacks import ModelCheckpoint
from keras.utils import to_categorical
from keras.regularizers import l1_l2
from input_para import input_from
from sklearn.metrics import confusion_matrix
import numpy as np
import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt

EPOCHS = 30


def shuffle(a, b):
    assert(a.shape[0] == b.shape[0])
    n = a.shape[0]
    shuffled = np.random.permutation(n)
    return (a[shuffled], b[shuffled])


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
                            batch_input_shape=(64, 40, 430, 1),
                            kernel_regularizer=l1_l2(l1=0.001, l2=0.001)))
    model.add(layers.MaxPooling2D(2, 2))
    model.add(layers.Conv2D(32, (3, 3), activation='relu',
                            kernel_regularizer=l1_l2(l1=0.001, l2=0.001)))
    model.add(layers.MaxPooling2D(2, 2))
    model.add(layers.Conv2D(64, (3, 3), activation='relu',
                            kernel_regularizer=l1_l2(l1=0.001, l2=0.001)))

    # CNN to RNN
    model.add(layers.Reshape(target_shape=(6, 104*64)))
    model.add(layers.Dense(64, activation='relu'))

    # RNN layer
    model.add(layers.LSTM(64, return_sequences=True, stateful=True,
                          batch_input_shape=(64, 6, 64),
                          kernel_regularizer=l1_l2(0.001, 0.001)))
    model.add(layers.LSTM(64, return_sequences=True, stateful=True,
                          batch_input_shape=(64, 6, 64),
                          kernel_regularizer=l1_l2(0.001, 0.001)))
    # convert 3D to 1D
    model.add(layers.Flatten())

    # fully-connected layer
    model.add(layers.Dense(64, activation='relu',
                           kernel_regularizer=l1_l2(0.001, 0.001)))
    model.add(layers.Dropout(0.5))
    model.add(layers.Dense(5, activation='softmax',
                           kernel_regularizer=l1_l2(0.001, 0.001)))

    # reshape data, scalling into [0, 1]
    train_images = x_train.reshape((x_train.shape[0], 40, 430, 1))
    train_images = train_images.astype('float32')/255
    val_images = x_val.reshape((x_val.shape[0], 40, 430, 1))
    val_images = val_images.astype('float32')/255
    test_images = x_test.reshape((x_test.shape[0], 40, 430, 1))
    test_images = test_images.astype('float32')/255

    # categorically encode the labels
    # Converts a class vector (integers) to binary class matrix
    train_labels = to_categorical(y_train)
    val_labels = to_categorical(y_val)
    test_labels = to_categorical(y_test)

    # Shuffle data
    train_images, train_labels = shuffle(train_images, train_labels)
    val_images, val_labels = shuffle(val_images, val_labels)
    test_images, test_labels = shuffle(test_images, test_labels)

    # Before training a model, you need to configure the learning process,
    model.compile(optimizer='rmsprop',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])
    model.summary()
    # For a multi-class classification problem
    # if there are saved, load the weights
    try:
        model.load_weights("weights-crnn.hdf5")
    except (OSError):
        print("No weights saved. Will train from scratch")
    except (ValueError):
        print("Network changed from the last saved weights. ",
              "Will train from scratch")

    checkpoint = ModelCheckpoint("weights-crnn.hdf5", save_best_only=True)

    # training use fit
    history = model.fit(train_images[:3136], train_labels[:3136],
                        epochs=EPOCHS, batch_size=64,
                        validation_data=(val_images[:256], val_labels[:256]),
                        callbacks=[checkpoint])
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

    model.load_weights("weights-crnn.hdf5")

    # evaluate
    test_loss, test_acc = model.evaluate(test_images[:512], test_labels[:512],
                                         batch_size=64)
    y_pred = model.predict(test_images[:512], batch_size=64)
    print(y_pred.shape)
    y_pred_mod = np.argmax(y_pred, axis=-1)
    y_test_mod = np.argmax(test_labels[:512], axis=-1)
    cnf_matrix = confusion_matrix(y_test_mod, y_pred_mod)
    print(cnf_matrix)
    print(test_acc)


if __name__ == '__main__':
    main()

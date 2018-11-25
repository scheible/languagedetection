#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  2 11:50:53 2018

@author: qiany
"""
import librosa
import numpy as np
from librosa import display
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from os import listdir, walk

def input_from(folder):
    split = 0.7
    lang_idx = 0
    lables = {}
    X_train = []
    X_test = []
    y_train = np.zeros(0)
    y_test = np.zeros(0)
    for dir, _, files in walk(folder):
        X = []
        y = np.zeros(0)
        for f in files:
            if f[-3:] != "wav":
                continue
            d, sr = librosa.load(dir + "/" + f)
            # mfcc
            mfccs = librosa.feature.mfcc(y=d, sr=sr, n_mfcc=40)
            print(mfccs)
            X.append(mfccs)
            if dir not in lables:
                lables[dir] = lang_idx
                lang_idx += 1
            y = np.append(y, lables[dir])
        X_train.extend(X[:int(split*len(X))])
        print(X_train)
        X_test.extend(X[int(split*len(X)):])
        y_train = np.append(y_train, y[:int(split*y.shape[0])])
        y_test = np.append(y_test, y[int(split*y.shape[0]):])
    
    idx = 0
    min = 100000000
    for a in X_train:
        if a.shape[1] < min:
            min = a.shape[1]
    
    x_train = np.zeros((len(X_train), 40, min))
    x_test = np.zeros((len(X_test), 40, min))
    for arr in X_train:
        x_train[idx, :, :] = arr[:, :min]
        idx += 1
    idx = 0
    for arr in X_test:
        x_test[idx, :, :] = arr[:, :min]
        idx += 1
        
    return ((x_train, y_train), (x_test, y_test))

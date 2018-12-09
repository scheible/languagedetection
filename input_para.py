#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  2 11:50:53 2018

@author: qiany
"""
import librosa
import numpy as np
from os import walk


def input_from(folder):
    test_split = 0.5
    val_split = 0.8
    lang_idx = 0
    lables = {}
    X_train = []
    X_val = []
    X_test = []
    y_train = np.zeros(0)
    y_val = np.zeros(0)
    y_test = np.zeros(0)

    streams = {}

    for dir, _, files in walk(folder, followlinks=True):
        for f in files:
            if f[-3:] != "wav":
                continue
            if dir not in files:
                streams[dir] = []
            d, sr = librosa.load(dir + "/" + f)
            streams[dir].append((d, sr))
    for dir in streams:
        for i, (d, sr) in enumerate(streams[dir]):
            # augment only the training set
            if i < test_split * val_split * len(streams[dir]):
                for speed in [0.9, 1, 1.1]:
                    x1 = d.copy()
                    t = librosa.effects.time_stretch(d, speed)
                    # keep same length as original;
                    minlen = min(x1.shape[0], t.shape[0])
                    x1 *= 0                                    # pad with zeros
                    x1[0:minlen] = t[0:minlen]
                    # mfcc
                    mfccs = librosa.feature.mfcc(y=x1, sr=sr, n_mfcc=40)
                    # print(mfccs)
                    X_train.append(mfccs)
                    if dir not in lables:
                        lables[dir] = lang_idx
                        lang_idx += 1
                    y_train = np.append(y_train, lables[dir])
            elif i < test_split * len(streams[dir]):
                mfccs = librosa.feature.mfcc(y=d, sr=sr, n_mfcc=40)
                X_val.append(mfccs)
                y_val = np.append(y_val, lables[dir])
            else:
                mfccs = librosa.feature.mfcc(y=d, sr=sr, n_mfcc=40)
                X_test.append(mfccs)
                y_test.append(lables[dir])
    
    idx = 0
    min = 100000000
    for a in X_train:
        if a.shape[1] < min:
            min = a.shape[1]
    for a in X_val:
        if a.shape[1] < min:
            min = a.shape[1]
    for a in X_test:
        if a.shape[1] < min:
            min = a.shape[1]
    
    x_train = np.zeros((len(X_train), 40, min))
    x_val = np.zeros((len(X_val), 40, min))
    x_test = np.zeros((len(X_test), 40, min))

    idx = 0
    for arr in X_train:
        x_train[idx, :, :] = arr[:, :min]
        idx += 1
    idx = 0
    for arr in X_val:
        x_val[idx, :, :] = arr[:, :min]
        idx += 1
    idx = 0
    for arr in X_test:
        x_test[idx, :, :] = arr[:, :min]
        idx += 1

    return ((x_train, y_train), (x_val, y_val), (x_test, y_test))

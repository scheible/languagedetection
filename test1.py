#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  2 11:50:53 2018

@author: qiany
"""
import librosa
from librosa import display
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from os import listdir, walk

X = []
lang_idx = 0
y = np.zeros(0)
lables = {}
for dir, _, files in walk("training_data"):
    for f in files:
        if f[-3:] != "wav":
            continue
        # print(dir)
        d, sr = librosa.load(dir + "/" + f)
        y = np.append(y, lables[dir])
        # mfcc
        mfccs = librosa.feature.mfcc(y=d, sr=sr, n_mfcc=40)
        print(mfccs.shape)
        X.append(mfccs)
        if dir not in lables:
            lables[dir] = lang_idx
            lang_idx += 1

idx = 0
min = 100000000
for a in X:
    if a.shape[1] < min:
        min = a.shape[1]

x = np.zeros((len(X), 93, min))
for arr in X:
    x[idx, :, :] = arr[:, :min]
    idx += 1

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

d,sr=librosa.load("eng_test\en-0532.wav" )
#print(d)
#librosa.display.specshow(d)

#spectrogram
D = librosa.amplitude_to_db(
        np.abs(librosa.stft(d,
                            n_fft=184, hop_length=96)),
                            ref=np.max)
librosa.display.specshow(D, y_axis='log')
plt.colorbar(format='%+2.0f dB')
plt.title('Linear-frequency power spectrogram')
plt.show()
plt.figure()
CQT = librosa.amplitude_to_db(np.abs(librosa.cqt(d, sr=sr)), ref=np.max)
librosa.display.specshow(CQT, y_axis='cqt_note')

#mfcc
mfccs = librosa.feature.mfcc(y=d, sr=sr, n_mfcc=40)
librosa.display.specshow(mfccs, x_axis='time')
plt.colorbar()
plt.title('MFCC')
plt.tight_layout()
plt.show()
#!/usr/bin/python3
import urllib
import os, sys, tarfile 

def main():
    base = "http://www.repository.voxforge1.org/downloads/it/SpeechCorpus/Trunk/Audio/Main/8kHz_16bit/"
    wanted = ["AR4CAD-20130328-lki.tgz"]
    for f in wanted:
        (filename, _) = urllib.urlretrieve(base+f)
        tar = tarfile.open(filename)
        for item in tar:
            print(item)

if __name__ == '__main__':
    main()

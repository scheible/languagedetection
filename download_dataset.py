#!/usr/bin/python3
from urllib import request
import os, sys, tarfile


def main():
    base = "http://www.repository.voxforge1.org/downloads/it/Trunk/Audio/Main/8kHz_16bit/"
    wanted = ["AR4CAD-20130328-lki.tgz"]
    for f in wanted:
        print(base+f)
        (filename, _) = request.urlretrieve(base+f)
        tar = tarfile.open(filename)
        # ectract the wav
        for item in tar:
            if item.name[-3:] == "wav":
                content = tar.extractfile(item)
                print(content)
            

if __name__ == '__main__':
    main()

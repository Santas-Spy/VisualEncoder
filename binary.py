import numpy as np
from math import sqrt

VERSION = '1.2.0'

'''
Contains functions common to both bits and bytes
'''

def çreateFileHeader(fileName):
    with open(fileName, 'rb') as f:
        fileBytes = f.read()
    fileType = fileName.split('.')[1] + '\t'
    versionNumber = VERSION + '\n'
    prefix = fileType + versionNumber
    prefixBytes = prefix.encode('raw_unicode_escape')
    byteArray = prefixBytes + fileBytes
    return byteArray

def createIntArray(fileName):
    byteArray = çreateFileHeader(fileName)
    intArray = np.frombuffer(byteArray, dtype=np.uint8)
    return intArray

def createBlankImage(intArray, compress):
    numBytes = len(intArray)
    dim = int(sqrt(numBytes/compress))+1
    print("Generating an image of size {} x {} using new format".format(dim, dim))
    img = np.zeros(shape=[dim,dim,3], dtype=np.uint8)
    return img, dim

def getData(raw):
    index = raw.index(b'\n')
    prefixData = '.' + raw[:index].decode('utf-8')
    data = raw[index+1:]
    prefix = prefixData.split('\t')
    extension = prefix[0]
    try:
        version = prefix[1]
    except IndexError:
        version = 'old'
    versionWarning(version)
    return extension, data

def encodeData(string, fileBytes):
    numBytes = len(fileBytes)
    for i, byte in enumerate(fileBytes):
        string += bin(byte)[2:].rjust(8, '0')
        if (numBytes > 10000):
            print("Encoding File. Progress: {:.2f}%".format(i*100/numBytes), end='\r')
    return string

def versionWarning(version):
    if version == 'old':
        print("Warning. A version number could not be found. This image was likely encoded using version 1.1.1 or lower")
        print("This may result in a corrupted output if the decoding process has changed")
    elif version != VERSION:
        print("[WARNING]: This image was encoded using version {}, but you are running version {}".format(version, VERSION))
        print("           If your result is corrupted the decoding process may have changed. Try again with the matching version")
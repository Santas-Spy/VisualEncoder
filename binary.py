import numpy as np
import encryption
import math
from numba import njit
from PIL import Image

VERSION = '1.2.1'

'''
Contains functions common to both bits and bytes
'''

def çreateFileHeader(fileName, password):
    with open(fileName, 'rb') as f:
        fileBytes = f.read()

    fileType = fileName.split('.')[1] + '\t'
    versionNumber = VERSION + '\t'
    if password != None and password != '':
        encrypted = 'locked\n'
        fileBytes = encryption.encrypt(password, fileBytes)
    else:
        encrypted = 'unlocked\n'

    prefix = fileType + versionNumber + encrypted
    prefixBytes = prefix.encode('raw_unicode_escape')
    print("Length of prefix bytes: " + str(len(prefixBytes)))
    byteArray = prefixBytes + fileBytes
    return byteArray

def createIntArray(fileName, password):
    byteArray = çreateFileHeader(fileName, password)
    intArray = np.frombuffer(byteArray, dtype=np.uint8)
    return intArray

def createBlankImage(intArray, compress):
    numBytes = len(intArray)
    dim = math.ceil(math.sqrt(numBytes/compress))
    print("Generating an image of size {} x {} using new format".format(dim, dim))
    img = np.zeros(shape=[dim,dim,3], dtype=np.uint8)
    return img, dim

def prepImage(fileName):
    image = Image.open(fileName)
    img = np.array(image)
    size = img.shape[0] * img.shape[1]
    finalPos = 0
    width = img.shape[0]
    
    #find where the data ends
    for i in range(size-1, 0, -1):
        [x, y] = getPos(i, width)
        if not (img[x,y] == [0, 0, 0]).all():
            finalPos = i
            break
    
    return img, finalPos, width

@njit
def getPos(pos, width):
    x = int(pos / width)
    y = int(pos % width)
    return [x, y]

def getData(raw):
    index = raw.index(b'\n')
    prefixData = '.' + raw[:index].decode('utf-8')
    data = raw[index+1:]

    #get header info
    prefix = prefixData.split('\t')
    extension = prefix[0]
    version = prefix[1]
    encrypted = prefix[2]

    if encrypted == 'locked':
        password = input("\nThis file is password protected. Please input the password: ")
        data = encryption.decrypt(password, data)

    versionWarning(version)
    return extension, data

def versionWarning(version):
    if version == 'old':
        print("\n\033[31m[WARNING]:\033[0m A version number could not be found. This image was likely encoded using version 1.1.1 or lower")
        print("This may result in a corrupted output if the decoding process has changed")
        print("You can download the latest version here: https://github.com/Santas-Spy/VisualEncoder/releases/tag/v" + VERSION + "\n")
    elif version != VERSION:
        print("\n\033[31m[WARNING]:\033[0m This image was encoded using version {}, but you are running version {}".format(version, VERSION))
        print("           If your result is corrupted the decoding process may have changed. Try again with the matching version")
        print("           You can download the correct version from here: https://github.com/Santas-Spy/VisualEncoder/releases/tag/v" + version + "\n")
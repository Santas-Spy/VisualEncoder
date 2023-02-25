import numpy as np
from math import sqrt
from numba import njit
from cv2 import imread

def fastFileToImage(fileName):
    #generate the val array
    with open(fileName, 'rb') as f:
        fileBytes = f.read()
    prefix = fileName.split('.')[1] + '\n'
    prefixBytes = prefix.encode('raw_unicode_escape')
    byteArray = prefixBytes + fileBytes
    intArray = np.frombuffer(byteArray, dtype=np.uint8)

    #build a blank image
    numBytes = len(intArray)
    dim = int(sqrt(numBytes/3))+1
    print("Generating an image of size {} x {}".format(dim, dim))
    img = np.zeros(shape=[dim,dim,3], dtype=np.uint8)

    img = placePixels(img, intArray, dim)
    return img

@njit
def placePixels(img, intArray, dim):
    i = 0
    intArray = np.copy(intArray)
    pixel = np.array([0, 0, 0])
    posCounter = 0
    pixelCounter = 0

    #for each value, assign it to a colour channel
    for val in intArray:
        pixel[pixelCounter] = val
        pixelCounter += 1
        if pixelCounter == 3:
            #all colour channels are full for this pixel, place it on the image
            [x,y] = getPos(posCounter, dim)
            img[x,y] = pixel
            pixel = np.array([0, 0, 0])
            posCounter += 1
            pixelCounter = 0
        i += 1
    
    #make sure we place the last pixel
    [x,y] = getPos(posCounter, dim)
    img[x,y] = pixel
    return img

@njit
def getPos(pos, width):
    x = int(pos / width)
    y = int(pos % width)
    return [x, y]

#get a series of bytes of out an image
def readImage(fileName):
    img = imread(fileName)
    size = img.shape[0] * img.shape[1]
    bits = ''
    finalPos = 0
    width = img.shape[0]
    
    #find where the data ends
    for i in range(size-1, 0, -1):
        [x, y] = getPos(i, width)
        if not (img[x,y] == [0, 0, 0]).all():
            finalPos = i
            break
    
    #read the data
    for i in range(finalPos):
        [x, y] = getPos(i, width)
        for val in img[x,y]:
            bits += bin(val)[2:].rjust(8, '0')
        print("Decoding Progress: {:.2f}%".format(100*i/finalPos), end='\r')
    
    #do the final pixel last incase it's only half full
    [x, y] = getPos(finalPos, width)
    for val in img[x,y]:
        if val != 0:
            bits += bin(val)[2:].rjust(8, '0')
    
    #convert the data to a bytearray
    data = bytearray(int(bits[i:i+8], 2) for i in range(0, len(bits), 8))
    return data
import numpy as np
from math import sqrt
from numba import njit
from cv2 import imread
import binary

@njit
def getPos(pos, width):
    x = int(pos / width)
    y = int(pos % width)
    return [x, y]

def fastFileToImage(fileName):
    #generate the val array
    intArray = binary.createIntArray(fileName)
    img, dim = binary.createBlankImage(intArray, 1)
    img = placePixels(img, intArray, dim)
    return img

@njit
def placePixels(img, intArray, dim):
    intArray = np.copy(intArray)
    pixel = np.array([0, 0, 0])
    posCounter = 0

    #for each value, set all colour channels to that value
    for val in intArray:
        [x,y] = getPos(posCounter, dim)
        img[x,y] = [val, val, val]
        posCounter += 1
    
    #make sure we place the last pixel
    [x,y] = getPos(posCounter, dim)
    img[x,y] = pixel
    return img

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
        val = img[x, y][0]
        bits += bin(val)[2:].rjust(8, '0')
        print("Decoding Progress: {:.2f}%".format(100*i/finalPos), end='\r')
    
    #convert the data to a bytearray
    data = bytearray(int(bits[i:i+8], 2) for i in range(0, len(bits), 8))
    print("Decoding complete")
    return data
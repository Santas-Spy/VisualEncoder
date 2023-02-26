import numpy as np
from numba import njit
import binary

def fastFileToImage(fileName, password):
    #generate the val array
    intArray = binary.createIntArray(fileName, password)
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
        [x,y] = binary.getPos(posCounter, dim)
        img[x,y] = [val, val, val]
        posCounter += 1
    
    #make sure we place the last pixel
    [x,y] = binary.getPos(posCounter, dim)
    img[x,y] = pixel
    return img

def readImage(fileName):
    img, finalPos, width = binary.prepImage(fileName)
    bits = ''

    #read the data
    for i in range(finalPos):
        [x, y] = binary.getPos(i, width)
        val = img[x, y][0]
        bits += bin(val)[2:].rjust(8, '0')
        print("Decoding Progress: {:.2f}%".format(100*i/finalPos), end='\r')
    print("Decoding Progress: 100.00%")
    
    #convert the data to a bytearray
    data = bytearray(int(bits[i:i+8], 2) for i in range(0, len(bits), 8))
    print("\033[32mDecoding complete\033[0m")
    return data
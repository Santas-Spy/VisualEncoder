import numpy as np
from numba import njit
import binary

def fastFileToImage(fileName, password):
    #generate the val array
    intArray = binary.createIntArray(fileName, password)
    img, dim = binary.createBlankImage(intArray, 3)
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
            [x,y] = binary.getPos(posCounter, dim)
            img[x,y] = pixel
            pixel = np.array([0, 0, 0])
            posCounter += 1
            pixelCounter = 0
        i += 1
    
    #make sure we place the last pixel
    [x,y] = binary.getPos(posCounter, dim)
    img[x,y] = pixel
    return img

#get a series of bytes of out an image
def readImage(fileName):
    img, finalPos, width = binary.prepImage(fileName)
    bits = ''
    
    #read the data
    for i in range(finalPos):
        [x, y] = binary.getPos(i, width)
        for val in img[x,y]:
            bits += bin(val)[2:].rjust(8, '0')
        print("Decoding Progress: {:.2f}%".format(100*i/finalPos), end='\r')
    
    #do the final pixel last incase it's only half full
    [x, y] = binary.getPos(finalPos, width)
    for val in img[x,y]:
        if val != 0:
            bits += bin(val)[2:].rjust(8, '0')
    print("Decoding Progress: 100.00%")
    
    #convert the data to a bytearray
    data = bytearray(int(bits[i:i+8], 2) for i in range(0, len(bits), 8))
    print("\033[32mDecoding complete\033[0m")
    return data
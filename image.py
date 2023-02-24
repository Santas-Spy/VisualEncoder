from cv2 import imread, imwrite
import numpy as np
from math import sqrt
from numba import njit

'''
helper functions
'''
def getPos(pos, width):
    x = int(pos / width)
    y = int(pos % width)
    return [x, y]

def imageToBits(fileName):
    img = imread(fileName)
    size = len(img[0]) * len(img)
    bits = getBits(img, size)
    data = bytearray(int(bits[i:i+8], 2) for i in range(0, len(bits), 8))

    return data

def imageToBytes(fileName):
    img = imread(fileName)
    size = len(img[0]) * len(img)
    bits = getBytes(img, size)
    data = bytearray(int(bits[i:i+8], 2) for i in range(0, len(bits), 8))

    return data

'''
functions for working in bits
'''
#convert an image into a string of 0's and 1's
def getBits(img, size):
    bits = ''
    finished = False
    count = 0
    for row in img:
        for pixel in row:
            if (finished == False):
                [r, g, b] = pixel
                if ([r, g, b] == [255, 255, 255]):
                    bits += '1'
                elif ([r, g, b] == [0, 0, 255]):
                    finished = True
                else:
                    bits += '0'
                count += 1
                print("Decoding Progress: {:.2f}%".format(100*count/size), end='\r')
    return bits

#convert a string of 0's and 1's into a black and white image
def bitsToImage(bits):
    dim = int(sqrt(len(bits)))+1

    print("Generating an image of size {} x {}".format(dim, dim))

    img = np.zeros(shape=[dim,dim,3], dtype=np.uint8)

    counter = 0
    for bit in bits:
        if bit == '1':
            [x, y] = getPos(counter, dim)
            img[x, y] = [255, 255, 255]
        counter += 1
        print("Image Printing Progress: {:.2f}%".format(100*counter/len(bits)), end='\r')
    [x, y] = getPos(counter, dim)
    img[x, y] = [0, 0, 255]
    return img

'''
Functions for working with Bytes
'''
#get a series of bytes of out an image
def getBytes(img, size):
    bits = ''
    finalPos = 0
    width = img.shape[0]

    for i in range(size-1, 0, -1):
        [x, y] = getPos(i, width)
        if not (img[x,y] == [0, 0, 0]).all():
            finalPos = size-i
            break
    
    for i in range(finalPos):
        [x, y] = getPos(i, width)
        for val in img[x,y]:
            bits += bin(val)[2:].rjust(8, '0')
        print("Decoding Progress: {:.2f}%".format(100*i/finalPos), end='\r')
    return bits

#turn a series of bytes into an rgb image
def bytesToImage(bits):
    dim = int(sqrt(len(bits)/24))+1
    print("Generating an image of size {} x {}".format(dim, dim))
    img = np.zeros(shape=[dim,dim,3], dtype=np.uint8)

    posCounter = 0
    pixel = []
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        val = int(byte, 2)
        pixel.append(val)
        if len(pixel) == 3:
            #we have filled a pixel, place it onto the image
            [x,y] = getPos(posCounter, dim)
            img[x,y] = pixel
            posCounter += 1
            pixel = []
        print("Image Printing Progress: {:.2f}%".format(100*i/len(bits)), end='\r')
    
    #pad a delimiter to the end of the data
    for i in range(3):
        pixel.append(0)
        if len(pixel) == 3:
            [x,y] = getPos(posCounter, dim)
            img[x,y] = pixel
            posCounter += 1
            pixel = []

    print("Did {} length data in {} pixels".format(len(bits), posCounter))
    return img
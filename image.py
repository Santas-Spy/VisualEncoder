from cv2 import imread, imwrite
import numpy as np
from math import sqrt
from numba import njit

def bitsToImage(bits):
    print(len(bits))
    dim = int(sqrt(len(bits)))+1

    print("Generating an image of size {} x {}".format(dim, dim))

    img = np.zeros(shape=[dim,dim,3], dtype=np.uint8)

    counter = 0
    for bit in bits:
        if bit == '1':
            [x, y] = getPos(counter, dim)
            img[x, y] = [255, 255, 255]
        counter += 1
    [x, y] = getPos(counter, dim)
    img[x, y] = [0, 0, 255]
    return img

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

#@njit
def getBits(img, size):
    bits = ''
    finished = False
    count = 0
    for row in img:
        for bit in row:
            if (finished == False):
                [r, g, b] = bit
                if ([r, g, b] == [255, 255, 255]):
                    bits += '1'
                elif ([r, g, b] == [0, 0, 255]):
                    finished = True
                else:
                    bits += '0'
                count += 1
                print("Decoding Progress: {:.2f}%".format(100*count/size), end='\r')
    return bits
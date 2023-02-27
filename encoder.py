import numpy as np
import binary
from PIL import Image
from numba import njit

def encode(fileName, codec):
    #get password
    password = input("Would you like to encrypt the file using a password? (Leave blank for no): ")
    
    intArray = binary.createIntArray(fileName, password)

    #generate an image using bits or bytes
    if (codec == '1'):
        #Black and white
        img, dim = binary.createBlankImage(intArray, 1)
        img = paintInBW(img, intArray, dim)
    else:
        #colour
        img, dim = binary.createBlankImage(intArray, 3)
        img = paintInColour(img, intArray, dim)
    
    #save the image
    name = fileName.split('.')[0] + "_encoded.png"
    pilImg = Image.fromarray(np.uint8(img))
    pilImg.save(name)
    print("Finished. Encoded image saved as " + name)

@njit
def paintInColour(img, intArray, dim):
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

@njit
def paintInBW(img, intArray, dim):
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
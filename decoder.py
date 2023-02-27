import binary
import zlib

def decode(fileName, codec):
    img, finalPos, width = binary.prepImage(fileName)
    if codec == '1':
        bits = readBW(finalPos, width, img)
    else:
        bits = readColour(finalPos, width, img)
    print("Decoding Progress: 100.00%")
    
    #convert the data to a bytearray
    data = bytearray(int(bits[i:i+8], 2) for i in range(0, len(bits), 8))
    decompressedData = zlib.decompress(data)
    print("\033[32mDecoding complete\033[0m")

    extension, data = binary.getData(decompressedData)
    if data != None:
        #convert the usable data into a file
        finalFileName = fileName.split('.')[0] + "_decoded" + extension
        with open(finalFileName, 'wb') as f:
            f.write(data)
        
        print("Finished. File saved as " + finalFileName)
    return data

def readColour(finalPos, width, img):
    bits = ''
    sanityChecker = 0
    checkWarningShowed = False
    for i in range(finalPos):
        [x, y] = binary.getPos(i, width)
        for val in img[x,y]:
            bits += bin(val)[2:].rjust(8, '0')
        
        if img[x,y][0] == img[x,y][1] and img[x,y][0] == img[x,y][1]:
            sanityChecker += 1
        else:
            sanityChecker = 0

        if sanityChecker >= 10 and checkWarningShowed == False:
            print("[WARNING]: It looks like your trying to decode a black and white file using RGB. This will result in a corrupted output as each bit of data is being read 3 times")
            checkWarningShowed = True

        print("Decoding Progress: {:.2f}%".format(100*i/finalPos), end='\r')
    
    #do the final pixel last incase it's only half full
    [x, y] = binary.getPos(finalPos, width)
    for val in img[x,y]:
        if val != 0:
            bits += bin(val)[2:].rjust(8, '0')
    return bits

def readBW(finalPos, width, img):
    bits = ''
    checkWarningShowed = False
    for i in range(finalPos):
        [x, y] = binary.getPos(i, width)
        val = img[x, y][0]
        sanity = img[x, y][1]

        if (sanity != val and checkWarningShowed == False):
            print("[WARNING]: It looks like your trying to decode an RGB file using black and white. This will result in a corrupted output as only 1/3 of the data has been read")
            checkWarningShowed = True

        bits += bin(val)[2:].rjust(8, '0')
        print("Decoding Progress: {:.2f}%".format(100*i/finalPos), end='\r')
    return bits
import binary

def decode(fileName, codec):
    img, finalPos, width = binary.prepImage(fileName)
    if codec == '1':
        bits = readBW(finalPos, width, img)
    else:
        bits = readColour(finalPos, width, img)
    print("Decoding Progress: 100.00%")
    
    #convert the data to a bytearray
    data = bytearray(int(bits[i:i+8], 2) for i in range(0, len(bits), 8))
    print("\033[32mDecoding complete\033[0m")

    extension, data = binary.getData(data)
    if data != None:
        #convert the usable data into a file
        finalFileName = fileName.split('.')[0] + "_decoded" + extension
        with open(finalFileName, 'wb') as f:
            f.write(data)
        
        print("Finished. File saved as " + finalFileName)
    return data

def readColour(finalPos, width, img):
    bits = ''
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
    return bits

def readBW(finalPos, width, img):
    bits = ''
    for i in range(finalPos):
        [x, y] = binary.getPos(i, width)
        val = img[x, y][0]
        bits += bin(val)[2:].rjust(8, '0')
        print("Decoding Progress: {:.2f}%".format(100*i/finalPos), end='\r')
    return bits
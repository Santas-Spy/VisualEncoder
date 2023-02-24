from numba import njit

def getBinaryString(fileName):
    with open(fileName, 'rb') as f:
        fileBytes = f.read()
    prefix = fileName.split('.')[1] + '\n'
    prefixBytes = prefix.encode('raw_unicode_escape')
    string = ''

    numBytes = len(fileBytes)

    for byte in prefixBytes:
        string += bin(byte)[2:].rjust(8, '0')

    string = encodeData(string, fileBytes)
    return string

def getData(raw):
    index = raw.find(b'\n')
    extension = '.' + raw[:index].decode('utf-8')
    data = raw[index+1:]
    return extension, data

def encodeData(string, fileBytes):
    numBytes = len(fileBytes)
    for i, byte in enumerate(fileBytes):
        string += bin(byte)[2:].rjust(8, '0')
        if (numBytes > 10000):
            print("Encoding File. Progress: {:.2f}%".format(i*100/numBytes), end='\r')
    return string
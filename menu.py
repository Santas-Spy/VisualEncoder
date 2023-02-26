import os

def getOperations():
    action = input("Select the action you wish to perform:\n\t[1]: Encode\n\t[2]: Decode\nChoice: ")
    if (action == '69'):
         print("nice.")
    while (action != '1' and action != '2' and action != '3'):
            action = input("That was invalid. Please select only 1 or 2: ")

    if (action == '1'):
        GET_FILE = "What is the name of the file you wish to encode: "
        fileName = input("What is the name of the file you wish to encode: ")
        while not os.path.isfile(fileName):
            print("That file did not exist or it was a directory. If you wish to encode a directory please zip it first.")
            fileName = input("What is the name of the file you wish to encode: ")
    elif (action == '2'):
        fileName = input("What is the name of the file you wish to decode: ")
        extension = fileName.split('.')[1]
        while not os.path.isfile(fileName) or extension != 'png':
            fileName = input("That file did not exist or was not a .png file. Please try again: ")
            extension = fileName.split('.')[1]
    else:
        GET_FILE = "WARNING! You are in automated testing mode"
        action = '3'
        fileName = 'input/image.png'
        codec = '1'
        return [action, fileName, codec]

    codec = input("Select the encoding type you wish to use:\n\t[1]: Black and White\n\t[2]: Colour\nChoice: ")
    while (codec != '1' and codec != '2'):
            codec = input("That was invalid. Please select only 1 or 2: ")

    return [action, fileName, codec]
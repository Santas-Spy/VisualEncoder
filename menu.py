import os

def getOperations():
    action = input("Select the action you wish to perform:\n\t[1]: Encode\n\t[2]: Decode\nChoice: ")
    while (action != '1' and action != '2'):
            action = input("That was invalid. Please select only 1 or 2: ")

    if (action == '1'):
        GET_FILE = "What is the name of the file you wish to encode: "
    else:
        GET_FILE = "What is the name of the file you wish to decode: "

    fileName =  input(GET_FILE)
    extension = fileName.split('.')[1]
    while not os.path.isfile(fileName) and extension != '.png':
        fileName = input("That file did not exist or was not a .png file. Please try again: ")
        extension = fileName.split('.')[1]

    return [action, fileName]
import binary, menu, bits, bytes
from cv2 import imwrite, imread

[action, file_name, codec] = menu.getOperations()

if (action == '1' or action == 'encode' or action == 'Encode'):
    #generate an image using bits or bytes
    if (codec == '1'):
        img = bits.fastFileToImage(file_name)
    else:
        img = bytes.fastFileToImage(file_name)
    
    #save the image
    name = file_name.split('.')[0] + "_encoded.png"
    imwrite(name, img)
    print("Finished. Encoded image saved as " + name)

elif (action == '2' or action == 'decode' or action == 'Decode'):
    #load the image
    
    #get the bits or bytes from an image
    if (codec == '1'):
        bits = bits.readImage(file_name)
    else:
        bits = bytes.readImage(file_name)
    
    #parse the bits and bytes into usable data
    extension, data = binary.getData(bits)

    #convert the usable data into a file
    final_file_name = file_name.split('.')[0] + "_decoded" + extension
    with open(final_file_name, 'wb') as f:
        f.write(data)
    
    print("Finished. File saved as " + final_file_name)

#testing mode used for 
elif (action == '3'):
    print("Entering testing mode")
    img = bits.fastFileToImage(file_name)
    name = file_name.split('.')[0] + "_encoded.png"
    imwrite(name, img)
    print("Finished. Encoded image saved as " + name)
else:
    print(str(action) + " was not a valid action")

input("Press Enter to exit...")
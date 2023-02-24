import image, binary, menu
from cv2 import imwrite

[action, file_name] = menu.getOperations()

if (action == '1' or action == 'encode' or action == 'Encode'):
    bit_string = binary.getBinaryString(file_name)
    img = image.bitsToImage(bit_string)
    name = file_name.split('.')[0] + "_encoded.png"
    imwrite(name, img)
    print("Finished. Encoded image saved as " + name)

elif (action == '2' or action == 'decode' or action == 'Decode'):
    bits = image.imageToBits(file_name)
    extension, data = binary.getData(bits)
    final_file_name = file_name.split('.')[0] + "_decoded" + extension
    with open(final_file_name, 'wb') as f:
        f.write(data)
    
    print("Finished. File saved as " + final_file_name)
else:
    print(str(action) + " was not a valid action")

input("Press Enter to exit...")
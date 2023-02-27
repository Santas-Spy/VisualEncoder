from PIL import Image
import numpy as np
import menu
from decoder import decode
from encoder import encode

[action, file_name, codec] = menu.getOperations()

if (action == '1' or action == 'encode' or action == 'Encode'):
    encode(file_name, codec)

elif (action == '2' or action == 'decode' or action == 'Decode'):
    decode(file_name, codec)

#testing mode used for automated testing
elif (action == '3'):
    print("Entering testing mode")
    print("Nothing to test")
else:
    print(str(action) + " was not a valid action")

input("Press Enter to exit...")
import binary, menu, bits, bytes
from PIL import Image
import numpy as np
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
    img = bits.fastFileToImage(file_name)
    name = file_name.split('.')[0] + "_encoded.png"
    pilImg = Image.fromarray(np.uint8(img))
    pilImg.save(name)
    print("Finished. Encoded image saved as " + name)
else:
    print(str(action) + " was not a valid action")

input("Press Enter to exit...")
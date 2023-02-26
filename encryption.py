from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import InvalidToken
import base64

def getKey(password):
    #salt = b"salt"  # A random value used to increase security
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,  # Key length in bytes
        salt=b"SaltyAsSeawater",
        iterations=100000,
    )
    key = kdf.derive(password.encode('utf-8'))
    strongKey = base64.urlsafe_b64encode(key)
    return strongKey

def encrypt(password, data):
    key = getKey(password)
    fernet = Fernet(key)
    encryptedData = fernet.encrypt(data)
    return encryptedData

def decrypt(password, data):
    key = getKey(password)
    fernet = Fernet(key)
    dataBytes = bytes(data)
    dataBytes += b'='       #I do not know why this is nessesary but without it the program cannot decrypt the data 🤷
    try:
        decryptedData = fernet.decrypt(dataBytes)
    except InvalidToken:
        print("\n\033[31mIncorrect Password\033[0m\n")
        return None
    return decryptedData
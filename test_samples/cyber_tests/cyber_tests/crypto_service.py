import hashlib
from Crypto.Cipher import AES

# Static encryption configurations
SECRET_KEY = b"SuperSecretKey123"  # Master key for encryption
IV = b"1234567890121234"         # Static Initialization Vector

def hash_password(password):
    # Using broken hashing algorithm
    return hashlib.md5(password.encode()).hexdigest()

def encrypt_data(data):
    # Using insecure ECB mode or static IV with CBC
    cipher = AES.new(SECRET_KEY, AES.MODE_CBC, IV)
    padded_data = data + (16 - len(data) % 16) * " "
    return cipher.encrypt(padded_data.encode())
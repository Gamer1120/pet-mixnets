import cryptography
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import padding as sympad

import requests
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os
import socket
import struct
import time
import poll
from time import gmtime, strftime

def sym_encrypt(message):
    # print("Starting symmetric encryption on message %s" % message)
    backend = default_backend()
    #16 bytes = 128 bits
    key = os.urandom(16)
    iv = os.urandom(16)
    padder = sympad.PKCS7(128).padder()
    padded_data = padder.update(message)
    padded_data += padder.finalize()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    # print("Encryption finished. key: %s iv: %s ciphertext %s" % (key, iv, ciphertext))
    return key, iv, ciphertext

def pub_encrypt(message, mixer_number):
    # print("Encrypting the message %s for mixer %i (PUBKEY)" % (message, mixer_number))
    with open("public-key-mix-" + str(mixer_number) + ".pem", "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )
        ciphertext = public_key.encrypt(message,
                                  padding.OAEP(
                                      mgf=padding.MGF1(algorithm=hashes.SHA1()),
                                      algorithm=hashes.SHA1(),
                                      label=None
                                  ))
        # print("Done encrypting. Ciphertext is %s"% ciphertext)
        return ciphertext

def full_encrypt(message):
    key3, iv3, ciphertext3= sym_encrypt(message)
    rsa3 = pub_encrypt(iv3 + key3, 3)
    e1 = rsa3 + ciphertext3
    key2, iv2, ciphertext2= sym_encrypt(e1)
    rsa2 = pub_encrypt(iv2 + key2, 2)
    e2 = rsa2 + ciphertext2
    key1, iv1, ciphertext1= sym_encrypt(e2)
    rsa1 = pub_encrypt(iv1 + key1, 1)
    e3 = rsa1 + ciphertext1

    return e3

# Set up connection
s = socket.socket()
host = "pets.ewi.utwente.nl"
port = 54179      
s.connect((host, port))

# Run test until n
n = 140

def countExits(n0):
    n, exits = poll.extractRemainder(poll.exitLogURI, n0)
    # Compensate for '(log is empty)' line
    if n == 1 and exits[0] == "(":
        return 0
    return n, exits

# Watch out for 'empty log' message
siz, exits = countExits(0)

for j in range(0, n):

    # Create a message
    m = str.encode('thresholdtest,' + str(j))
    c = full_encrypt(m)

    # Send the message
    s.send(struct.pack('>I', len(c)) + c)
    time.sleep(0.1)

    # Check for output
    siz, exits = countExits(siz)

    if(len(exits) > 0):
        print(j+1, "New exits: " + str(len(exits)))
        # print(exits)
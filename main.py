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
from time import gmtime, strftime

def sym_encrypt(message):
    print("Starting symmetric encryption on message %s" % message)
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
    print("Encryption finished. key: %s iv: %s ciphertext %s" % (key, iv, ciphertext))
    return key, iv, ciphertext

def pub_encrypt(message, mixer_number):
    print("Encrypting the message %s for mixer %i (PUBKEY)" % (message, mixer_number))
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
        print("Done encrypting. Ciphertext is %s"% ciphertext)
        return ciphertext

s = socket.socket()
host = "pets.ewi.utwente.nl"
port = 52604
s.connect((host, port))
i = range(1,42)
for j in i:
    messagearray = range(1,2)
    for message in messagearray:
        #    message = b"PETs,group 16."
        message = str.encode('thresholdtest,' + str(message) + " " + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + " " + str(j))
        key3, iv3, ciphertext3= sym_encrypt(message)
        rsa3 = pub_encrypt(iv3 + key3, 3)
        e1 = rsa3 + ciphertext3
        key2, iv2, ciphertext2= sym_encrypt(e1)
        rsa2 = pub_encrypt(iv2 + key2, 2)
        e2 = rsa2 + ciphertext2
        key1, iv1, ciphertext1= sym_encrypt(e2)
        rsa1 = pub_encrypt(iv1 + key1, 1)
        e3 = rsa1 + ciphertext1

        #print(requests.post("https://pets.ewi.utwente.nl:57523", str(len(e3)) + str(e3)))
        print("e3 is %s" % e3)

        s.send(struct.pack('>I', len(e3)) + e3)
        time.sleep(0.1)
        # data = s.recv(5)
        # print(data)
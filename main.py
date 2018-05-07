import cryptography
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
import requests
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os

def sym_encrypt(message):
    print("Starting symmetric encryption on message %s" % message)
    backend = default_backend()
    #32 bytes = 256 bits
    key = os.urandom(32)
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(message) + encryptor.finalize()
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
                                      mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                      algorithm=hashes.SHA256(),
                                      label=None
                                  ))
        print("Done encrypting. Ciphertext is %s"% ciphertext)
        return ciphertext


message = b"Alice,Hi Alice!."
key1, iv1, ciphertext1= sym_encrypt(message)
rsa1 = pub_encrypt(iv1 + key1, 1)
e1 = rsa1 + ciphertext1
key2, iv2, ciphertext2= sym_encrypt(e1)
rsa2 = pub_encrypt(iv2 + key2, 2)
e2 = rsa2 + ciphertext2
key3, iv3, ciphertext3= sym_encrypt(e2)
rsa3 = pub_encrypt(iv3 + key3, 3)
e3 = rsa3 + ciphertext3

print(requests.post("https://pets.ewi.utwente.nl:57523", str(len(e3)) + str(e3)))

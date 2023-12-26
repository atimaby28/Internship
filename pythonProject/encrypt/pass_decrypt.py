from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

import pickle


def dec_conn():
    private_key_file = open('encrypt/pem/private.pem', 'r')
    private_key = RSA.importKey(private_key_file.read(), passphrase='password')

    with open('encrypt/pickle/connection.pickle', 'rb') as f:
        encrypted = pickle.load(f)

    decryptor = PKCS1_OAEP.new(private_key)
    decryted = decryptor.decrypt(encrypted)

    private_key_file.close()

    return decryted.decode('utf-8')


def dec_dooray():
    private_key_file = open('encrypt/pem/private.pem', 'r')
    private_key = RSA.importKey(private_key_file.read(), passphrase='password')

    with open('encrypt/pickle/dooray.pickle', 'rb') as f:
        encrypted = pickle.load(f)

    decryptor = PKCS1_OAEP.new(private_key)
    decryted = decryptor.decrypt(encrypted)

    private_key_file.close()

    return decryted.decode('utf-8')


def dec_dooray_test():
    private_key_file = open('encrypt/pem/private.pem', 'r')
    private_key = RSA.importKey(private_key_file.read(), passphrase='password')

    with open('encrypt/pickle/dooray_test.pickle', 'rb') as f:
        encrypted = pickle.load(f)

    decryptor = PKCS1_OAEP.new(private_key)
    decryted = decryptor.decrypt(encrypted)

    private_key_file.close()

    return decryted.decode('utf-8')


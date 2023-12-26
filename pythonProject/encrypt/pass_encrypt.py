from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import PKCS1_OAEP

import sys
import pickle

pass_word = sys.argv[1]
pass_dir = sys.argv[2]

print(pass_word)
print (pass_dir)

public_key_file = open('encrypt/pem/public.pem', 'r')
public_key = RSA.importKey(public_key_file.read())

print(public_key_file)

plain_text = pass_word

random_func = Random.new().read
encryptor = PKCS1_OAEP.new(public_key)
encrypted = encryptor.encrypt(plain_text.encode('utf-8'))

pwd_dir = "encrypt/pem/" + pass_dir

with open(pwd_dir + ".pickle", 'wb') as f:
    pickle.dump(encrypted, f)

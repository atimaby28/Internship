from Crypto.PublicKey import RSA

rsa = RSA.generate(2048)
private_pem = rsa.exportKey(format='PEM', passphrase='password')

with open('./pem/private.pem', 'wb') as f:
    f.write(private_pem)

public_pem = rsa.public_key().exportKey()

with open('./pem/public.pem', 'wb') as f:
    f.write(public_pem)
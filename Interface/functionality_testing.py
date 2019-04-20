'''

This script demonstrates how to generate an ethereum account (address and key pair)
and how to encrypt and decrypt a message using the key pair. Something like this
will be used for ensuring that only approved parties will have access to the data.

'''

''' ACCOUNT GENERATION '''
from web3.auto import w3
from eth_keys import keys
from eth_utils import decode_hex

print("Web3 keypair")

# Generate ethereum account
acct =  w3.eth.account.create()

# extract public & private keys
prvk_hex = acct.privateKey.hex()
pubk_hex = keys.PrivateKey(acct.privateKey).public_key.to_hex()

# print address and key pair
print("address ", acct.address)
print("public key ", pubk_hex)
print("private key ", prvk_hex)

''' ENCRYPTION & DECRYPTION'''
from ecies import encrypt, decrypt

data = b' GURUMURUHURUBURUBURUNOMDOP '

# encrypt & decrypt data using ethereum key pair
encrypted = encrypt(pubk_hex, data)
decrypted = decrypt(prvk_hex, encrypted)

# print data, encrypted data and decrypted data
print()
print("data ", data)
print("encrypted data ", encrypted)
print("decrypted data ", decrypted)

''' DATA HASHING '''
import hashlib 

print(hashlib.sha224(b"Nobody inspects the spammish repetition").hexdigest())

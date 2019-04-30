'''
This script contains helpful functions for dealing with our interface, like

	- generate eth account (address and key pair)
 	- encrypt and decrypt data using the eth key pair
 	- hash data

'''

from web3.auto import w3
from eth_keys import keys
from eth_utils import decode_hex
from ecies import encrypt, decrypt
import hashlib 
import json

class Utilities:

	@staticmethod
	def generate_ethereum_keypair():
		# generate ethereum account
		acct =  w3.eth.account.create()
		# extract public & private keys
		prvk_hex = acct.privateKey.hex()
		pubk_hex = keys.PrivateKey(acct.privateKey).public_key.to_hex()
		return { "public_key": pubk_hex, "private_key": prvk_hex, "address": acct.address};

	@staticmethod
	def encrypt_data_using_public_key(public_key:str, data:dict):
		# encrypt data using ethereum public key
		return encrypt(public_key, data)
	
	@staticmethod
	def decrypt_data_using_private_key(private_key:str, data:dict):
		# decrypt data using ethereum private key
		return decrypt(private_key, data)

	@staticmethod
	def hash_data(data:dict):
		# print("TODO: Test performace for the different hashing algos.")
		# hash data
		return hashlib.sha224(json.dumps(data, sort_keys=True).encode()).hexdigest()
		#return hash(json.dumps(data, sort_keys=True))
		#return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()
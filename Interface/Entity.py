import json
from Interface.Utilities import Utilities

class Entity:

	def __init__(self, tier:int = 0, data:dict = {"general":{} }):
		# create eth key pair for agent
		account_info = Utilities.generate_ethereum_keypair()
		# add extra data fields
		data["general"]["tier"] = tier
		data["general"]["unique_id"] = account_info["address"]
		data["general"]["public_key"] = account_info["public_key"]
	 	# assign variables
		self.data = data
		self.unique_id = account_info["address"]
		self.public_key = account_info["public_key"]
		self.private_key = account_info["private_key"]
		# hash data
		self.data_hash = Utilities.hash_data(data)
		# define access rights
		self.has_access_to = { "agents" : [], "organizations": [], "devices":[] }

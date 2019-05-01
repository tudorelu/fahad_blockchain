import json
from Utilities import Utilities

class Agent:

	def __init__(self, account:str="", tier:int = 0, data:dict = {"general":{}}):

		if len(account) < 1:
			# create eth key pair for agent
			account_info = Utilities.generate_ethereum_keypair()
			data["general"]["public_key"] = account_info["public_key"]
			self.public_key = account_info["public_key"]
			self.private_key = account_info["private_key"]
		else:
			account_info = { "address": address }
		# add extra data fields
		data["general"]["tier"] = tier
		data["general"]["unique_id"] = account_info["address"]
		
		# assign variables
		self.data = data
		self.unique_id = account_info["address"]
		# hash data
		self.data_hash = Utilities.hash_data(self.data)
		# define access rights
		self.access_rights = { "agents" : {}, "organizations": {}, "devices":{}}

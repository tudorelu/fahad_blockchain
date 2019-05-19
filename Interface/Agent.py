import json
from Interface.Utilities import Utilities
#from Interface.Interface import ContractDatabaseInterface
from Interface.Constants import AccessType

class Agent:

	def __init__(self, interface:any, 
		tier:int=0, data:dict={"fname":"","lname":"","unique_id":"","data_1":{"entry_1":"","entry_2":"","subfolder_1":{},"subfolder_2":{}},"data_2":{"entry_1":"","entry_2":"","subfolder_1":{},"subfolder_2":{},},"data_3":{"entry_1":"","entry_2":"","subfolder_1":{},"subfolder_2":{},}}, 
		account_address:str=None, account_password:str=""):

		self.interface = interface
		
		if account_address == None:
			# create a new wallet/account
			self.unique_id = self.interface.w3.personal.newAccount("");	
		else:
			try:
				if self.interface.w3.personal.unlockAccount(account_address, account_password):
					self.unique_id = account_address
				else:
					self.unique_id = self.interface.w3.personal.newAccount("");
			except:
				self.unique_id = self.interface.w3.personal.newAccount("");

		# add extra data fields
		data["tier"] = tier
		data["unique_id"] = self.unique_id
		
		self.data = data
				
		# hash data
		self.data_hash = Utilities.hash_data(self.data)
		
		# define access rights
		self.has_access_to = { "agents" : [], "organizations": [], "devices":[] }

		if self.interface.contract_transact('createNewAgent', (self.unique_id, self.data_hash)):
			# save Agent details in database, after succesfully saving them on the blockchain
			self.interface.save_entity_data_to_database(self, root='agents')

		# put 10 eth into agent's account
		self.interface.w3.personal.sendTransaction({"to":self.unique_id, "from": self.interface.w3.personal.listAccounts[0], "value":self.interface.w3.toWei("1", "ether")}, "")

		# TODO: Have Option Which Reconstructs Agent From Blockchain and Database


	##### DATA INTEGRITY #####

	def has_data_integrity(self):
		""" Checks whether data of Agent has been tampered with, by comparing the 
		hash stored in the blockchain with the one resulted from the database.
		returns: True if data HAS NOT been tampered with, False otherwise """

		if not self.interface.contract_call('isAgent', (self.unique_id,)):
			print("Address doesn't appear as belonging to an Agent on this contract instance!")
			return -1;

		# get hash as saved on blockchain
		agent_blockchain_data = self.get_blockchain_details()
		blockchain_hash = agent_blockchain_data[2].hex().rstrip("0")
		#print("Blockchain hash is "+str(blockchain_hash))
		# get actual hash of database
		agent_database_data = self.get_database_details()
		database_hash = Utilities.hash_data(agent_database_data)
		#print("Database hash is "+database_hash)
		# compare
		return blockchain_hash == database_hash

	def get_database_details(self):
		""" Reads data of Agent from database """
		return self.interface.read_database_path(path=['agents', self.unique_id])

	def get_blockchain_details(self):
		""" Get data of Agent as stored on blockchain """
		return self.interface.contract_call('viewAgentDetails', (self.unique_id,))

	def validate_data_on_blockchain(self):
		""" Sets the Agent's hash on blockchain to his data's hash """
		data = self.get_database_details()
		data_hash = Utilities.hash_data(data)
		return self.interface.contract_transact('setAgentDataHash', (self.unique_id, data_hash), from_address=self.unique_id)

	##### ACCESS RIGHTS #####

	def give_agent_access_to_data(self, accessor_id:str, access_type:AccessType, data_path:str):
		""" Gives accessor_id access to agent's data """
		return self.interface.contract_transact('giveAgentAccessToData', args=(self.unique_id, accessor_id, access_type.value, data_path.encode("utf-8")), from_address=self.unique_id)

	def remove_agent_access_from_data(self, accessor_id:str, data_path:str):
		
		return self.interface.contract_transact('removeAgentAccessToData', args=(self.unique_id, accessor_id, data_path.encode("utf-8")), from_address=self.unique_id)

	def get_agent_access_rights_to_data(self, accessor_id:str, data_path:str):
		
		return self.interface.get_agent_access_rights_to_another_agent_data(owner_id=self.unique_id, accessor_id=accessor_id, data_path=data_path, from_address=self.unique_id)

	##### CHANGING STATE #####

	def read_agent_data_path(self, path:list, owner_id:str):

		if owner_id != self.unique_id:
			spath = ''
			for p in path[:-1]:
				spath = spath + p+'/'
			spath = spath + path[-1]

			access_right = self.interface.get_agent_access_rights_to_another_agent_data(accessor_id=self.unique_id, owner_id=owner_id, data_path=spath, from_address=owner_id)
			if access_right != 1 and access_right != 3:
				return None

		return self.interface.read_database_path(["agents", owner_id]+path)

	def write_to_agent_data_path(self, path:list, value:any, owner_id:str):
		
		access_right = 0

		if owner_id != self.unique_id:
			i = 1

			while access_right not in [2,3]:	
				if i >= len(path):
					return False

				newPath = path[:i]
				spath = ''
				
				for p in newPath[:-1]:
					spath = spath + p+'/'
				spath = spath + newPath[-1]

				print("checking access right for "+spath)
				access_right = self.interface.get_agent_access_rights_to_another_agent_data(accessor_id=self.unique_id, owner_id=owner_id, data_path=spath, from_address=owner_id)
				print("access right is "+str(access_right))

				i = i+1

		if not self.interface.write_to_database_path(["agents", owner_id] + path, value):
			return False

		return self.validate_data_on_blockchain()	

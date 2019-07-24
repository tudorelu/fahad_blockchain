'''
Written by Tudor Barbulescu. 

	Interface used to interact with smart contracts on the blockchain.

	This class defines an interface which enables the interaction between 
	an Ethereum smart contract and a locally stored SQL database. 

	The interface does two things: it conects to the Ethereum blockchain to
	enable the interaction with a specific contract, plus it also connects 
	to the database and interacts with it based on what is written in the 
	blockchain.

	The smart contract acts as an authentication layer on top of the database, 
	providing the access rights for Entiies to read and write to the database.

	The interface connects to the smart contract by using web3.py and to the
	database through the sqlite3 library.

	The database contains general information about th Entities involved in 
	the system. An Entity can either be an Individual (Agent) or an Organiza-
	tion. Entities should not have access to the entire database; instead, 
	they should only be allowed to access specific parts. These parts are 
	defined by the ACCESS RIGHTS module, which will be another database.
		
'''
import os
import sys
import json
import time
from web3 import Web3, HTTPProvider
from web3.auto import w3
from solcx import compile_source

curr_path = os.path.abspath(__file__)
root_path = os.path.abspath(os.path.join(curr_path, os.path.pardir, os.path.pardir))
sys.path.append(root_path)

from Interface.contract_source_code import source
from Interface.Agent import Agent
from Interface.Organization import Organization
from Interface.Device import Device
from Interface.Utilities import Utilities

class ContractDatabaseInterface:

	def __init__(self, contract_address:str=None, provider_link:str= "http://127.0.0.1:7545", time_it:bool=False,
		default_acct_address=None, default_acct_pass=""):
		
		self.time_it					= time_it
		
		if self.time_it:
			start = time.time()

		# this connects to the web3 provider (blockchain node)		
		self.w3 						= Web3(HTTPProvider(provider_link, request_kwargs={'timeout':60}))

		if self.time_it:
			end = time.time();
			print ("Connecting to w3 provider took  %.3f s " % (end - start));

		#self.w3.personal.unlockAccount(self.w3.eth.accounts[default_acct_number], default_acct_pass, '0x1000');
		if default_acct_address is not None:
			self.w3.eth.defaultAccount = self.w3.toChecksumAddress(default_acct_address)
		else:
			self.w3.eth.defaultAccount = self.w3.toChecksumAddress(self.w3.eth.accounts[0])
	
		print ("Default account is %s " % self.w3.eth.defaultAccount)
		# set pre-funded account as sender

		# either load a contract from address or instantiate a new one

		if self.time_it:
			start = time.time()
			
		if contract_address == None:
			self.contract_instance 		= self.create_new_contract_instance()

			if self.time_it:
				end = time.time();
				print ("Creating new contract instance took  %.3f s " % (end - start));
		else:
			self.contract_instance 		= self.get_contract_instance_from_address(self.w3.toChecksumAddress(contract_address));

			if self.time_it:
				end = time.time();
				print ("Loading contract instance from address took  %.3f s " % (end - start));

		# set the database path
		self.database_path 				= os.getcwd()+"/Database/database.json"

	#################### CONTRACT FUNCTIONS ######################

	def create_new_contract_instance(self):
		""" Create new contract instance from source code and deploy """
		# Solidity source code	
		compiled_sol = compile_source(source)
		contract_interface = compiled_sol['<stdin>:System']

		# Instantiate and deploy contract
		System = self.w3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])

		print("About to create contract...")
			
		tx_hash = System.constructor().transact()

		print("Getting Receipt...")

		# Wait for the transaction to be mined, and get the transaction receipt
		tx_receipt = self.w3.eth.waitForTransactionReceipt(tx_hash)
		print("tx_receipt")
		print(tx_receipt)

		self.contract_address = tx_receipt.contractAddress
		# Create the contract instance with the newly-deployed address
		return self.w3.eth.contract(
		    address=tx_receipt.contractAddress,
		    abi=contract_interface['abi'],
		)

	def get_contract_instance_from_address(self, contract_address):
		""" Get contract instance from address """
		
		self.contract_address = contract_address
		
		# Solidity source code	
		compiled_sol = compile_source(source)
		contract_interface = compiled_sol['<stdin>:System']
		
		# Load contract instance from address
		return self.w3.eth.contract(
		    address=contract_address,
		    abi=contract_interface['abi'],
		)

	def contract_transact(self, function_name:str, args:tuple=(), from_address:str=None, account_password="", await_receipt=True):
		""" Call contract function
		function_name : same of smart contract function to call
		returns : True if function call was succesfull, False otherwise """
		if self.time_it:
			start = time.time();
			
		if from_address == None:
			from_address = self.w3.eth.defaultAccount

		try:
			if not self.w3.personal.unlockAccount(from_address, account_password):
				print("Wrong password for unlocking account")
				return None
		except Exception as e:
			print(str(e))
			print("Error unlocking account")
			return None	

		tx_hash = self.contract_instance.functions[function_name](*args).transact({"from":from_address})
		
		if await_receipt:			
			tx_receipt = self.w3.eth.waitForTransactionReceipt(tx_hash)
			# print(tx_receipt)

			if self.time_it:
				end = time.time();
				print ("Calling " + function_name + " took  %.3f s " % (end - start));

			return tx_receipt['status'] == 1


	def contract_call(self, function_name:str, args:tuple=(), from_address:str=None, account_password=""):
		""" Call contract view function """
		if self.time_it:
			start = time.time();

		if from_address == None:
			from_address = self.w3.eth.defaultAccount
		
		try:
			if not self.w3.personal.unlockAccount(from_address, account_password):
				print("Wrong password for unlocking account")
				return None
		except Exception as e:
			print(str(e))
			print("Error unlocking account")	
			return None
		
		ret =  self.contract_instance.functions[function_name](*args).call({"from":from_address})

		if self.time_it:
			end = time.time();
			print ("Calling " + function_name + " took  %.3f s " % (end - start));

		return ret

	def get_agent_access_rights_to_another_agent_data(self, accessor_id:str, owner_id:str, data_path:str, from_address:str=None):
		""" Checks what kind of access rights does accessor_id have to owner_id's data_path """

		if from_address == None:
			from_address = accessor_id

		# print("Getting the access rights of "+accessor_id+" to "+owner_id+"'s' data, path "+data_path)
		return self.contract_call(function_name='getAgentAccessRightsToData', args=(owner_id, accessor_id, data_path.encode("utf-8")), from_address=from_address)
		
	#################### DATABASE FUNCTIONS ######################

	def save_entity_data_to_database(self, entity, root):
		""" Save data to database when new entity is created """
		path = [x for x in [root, entity.unique_id] if x is not None]
		self.write_to_database_path(path, entity.data)

	def read_database_path(self, path:list):
		"""Reads data within database path
		path: list of str, as ["path", "to", "data"]"""
		if self.time_it:
			start = time.time();

		with open(self.database_path, 'r') as f:	
			datastore = json.load(f)
			return Utilities.get_dict_by_path(datastore, path)

		if self.time_it:
			end = time.time();
			print ("Reading from DB took  %.3f s " % (end - start));

	def write_to_database_path(self, path:list, value:any):
		"""Writes data to the database path
		path: list of str, formatted as ["path", "to", "data"]"""
		datastore = {}
		
		if self.time_it:
			start = time.time();

		try:
			with open(self.database_path, 'r') as f:
				datastore = json.load(f)

			with open(self.database_path, 'w') as f:	
				Utilities.set_dict_by_path(datastore, path, value)
				f.write(json.dumps(datastore, indent=4))
		except:
			return False
			
		if self.time_it:
			end = time.time();
			print ("Writing to DB took  %.3f s " % (end - start));

		return True

	#################### ORGANIZATION FUNCTIONS ######################

	def create_organization(self, tier: int, admin_id: str, data: dict):
		""" Creates an Organization instance on blockchain and in the database """
		org = Organization(tier=tier, admin_id=admin_id, data=data)
		# add Org details to blockchain
		if self.contract_transact('createNewOrganization', (org.unique_id, admin_id, org.data_hash)):
			# save Org details in db
			self.save_entity_data_to_database(org, root='organizations')
			return org
		return None

	#################### DEVICE FUNCTIONS ######################

	def create_device(self, admin_id: str, data: dict):
		""" Creates a Device instance on blockchain and in the database"""
		dev = Device(admin_id=admin_id, data=data)
		# add Org details to blockchain
		if self.contract_transact('createNewDevice', (dev.unique_id, admin_id)):
			# save Org details in db
			self.save_entity_data_to_database(dev, root='devices')
			return dev
		return None

'''
	def create_agent(self, tier: int, data: dict):
		""" Creates an Agent instance in database and on blockchain
		returns: Agent instance if succesful, None otherwise"""
		agent = Agent(tier=tier, data=data)

		# save Agent details on blockchain
		if self.contract_transact('createNewAgent', (agent.unique_id, agent.data_hash)):
			# save Agent details in database (after succesfully saved them on blockchain)
			self.save_entity_data_to_database(agent, root='agents')
			return agent

		return None

	def create_agent_from_existing_account(self, tier: int, data: dict, account:str):
		""" Creates an Agent instance in database and on blockchain
		returns: Agent instance if succesful, None otherwise"""

		agent = Agent(tier=tier, data=data, account=account)

		# save Agent details on blockchain
		if self.contract_transact('createNewAgent', (agent.unique_id, agent.data_hash)):
			# save Agent details in database (after succesfully saved them on blockchain)
			self.save_entity_data_to_database(agent, root='agents')
			return agent

		return None

	def get_agent_blockchain_details(self, agent_address):
		""" Get data of Agent as stored on blockchain """
		return self.contract_call('viewAgentDetails', (agent_address,))

	def get_agent_database_details(self, agent_address):
		""" Reads data of Agent from database """
		return self.read_database_path(['agents', agent_address])

	def agent_data_integrity(self, agent_address):
		""" Checks whether data of Agent has been tampered with, by comparing the 
		hash stored in the blockchain with the one resulted from the database.
		returns: True if data HAS NOT been tampered with, False otherwise """

		if not self.contract_call('isAgent', (agent_address,)):
			print("Address doesn't appear as belonging to an Agent on this contract instance!")
			return -1;

		# get hash as saved on blockchain
		agent_blockchain_data = self.get_agent_blockchain_details(agent_address)
		blockchain_hash = agent_blockchain_data[2]

		# get actual hash of database
		agent_database_data = self.get_agent_database_details(agent_address)
		database_hash = Utilities.hash_data(agent_database_data)

		# compare
		return blockchain_hash == database_hash

	def validate_agent_data_on_blockchain(self, agent_address):
		""" Sets the Agent's hash on blockchain to his data's hash """
		data = self.get_agent_database_details(agent_address)
		data_hash = Utilities.hash_data(data)
		return self.contract_transact('setAgentDataHash', (agent_address, data_hash))

	def give_agent_access_to_another_agent_data(
		self, 
		accessor_id:str, 
		owner_id:str, 
		access_type:AccessType,
		data_path:str):
		
		return self.contract_transact('giveAgentAccessToData', (owner_id, accessor_id, access_type.value, data_path.encode("utf-8")))
	
	def remove_agent_access_to_another_agent_data(
		self, 
		accessor_id:str, 
		owner_id:str,
		data_path:str):
		
		return self.contract_transact('removeAgentAccessToData', (owner_id, accessor_id, data_path.encode("utf-8")))
'''


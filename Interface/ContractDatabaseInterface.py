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

Remember to run Ganache in parallel with running this interface. 

'''
import os
import json
import time
import operator
from web3 import Web3, HTTPProvider
from solcx import compile_source
from contract_source_code import source
from Agent import Agent
from Organization import Organization
from Utilities import Utilities
from functools import reduce 



class ContractDatabaseInterface:

	def __init__(self):
		# provider links
		self.infura_provider_link	= "http://kovan.infura.io/v3/3056875747b44d598630b4975043e928";
		self.local_provider_link	= "http://127.0.0.1:7545";

		# contract that the user will be interacting with
		self.w3 					= Web3(HTTPProvider(self.local_provider_link))
		
		# set pre-funded account as sender
		self.w3.eth.defaultAccount 	= self.w3.eth.accounts[0]

		#self.contract_instance 		= self.create_new_contract_instance()
		self.contract_instance 		= self.get_contract_instance_from_address('0x412310718117aD64db457A5FDBc161f498D17544');

		self.database_path = os.getcwd()+"/../Database/database.json"

	#################### CONTRACT FUNCTIONS ######################

	def create_new_contract_instance(self):
		""" Create new contract instance from source code and deploy """
		# Solidity source code	
		compiled_sol = compile_source(source)
		contract_interface = compiled_sol['<stdin>:System']

		# Instantiate and deploy contract
		System = self.w3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])

		# Submit the transaction that deploys the contract
		tx_hash = System.constructor().transact()

		# Wait for the transaction to be mined, and get the transaction receipt
		tx_receipt = self.w3.eth.waitForTransactionReceipt(tx_hash)

		# Create the contract instance with the newly-deployed address
		return self.w3.eth.contract(
		    address=tx_receipt.contractAddress,
		    abi=contract_interface['abi'],
		)

	def get_contract_instance_from_address(self, contract_address):
		""" Get comtract instance from address """
		# Solidity source code	
		compiled_sol = compile_source(source)
		contract_interface = compiled_sol['<stdin>:System']

		# Load contract instance from address
		return self.w3.eth.contract(
		    address=contract_address,
		    abi=contract_interface['abi'],
		)

	def contract_transact(self, function_name:str, args:tuple=()):
		""" Call contract function """
		''' Returns True if function call was succesfull, False otherwise '''
		tx_hash = ''

		if len(args) > 1:
			tx_hash = self.contract_instance.functions[function_name](*args).transact({'from':self.w3.eth.defaultAccount})
		else :
			tx_hash = self.contract_instance.functions[function_name](args).transact({'from':self.w3.eth.defaultAccount})

		tx_receipt = self.w3.eth.waitForTransactionReceipt(tx_hash)

		return tx_receipt['status'] == 1

	def contract_call(self, function_name:str, args:tuple=()):
		""" Call contract view function """
		return self.contract_instance.functions[function_name](args).call()

	#################### DATABASE FUNCTIONS ######################

	def save_entity_data_to_database(self, entity):
		""" Save data to database when new entity is created """
		datastore = {}
		# read current db
		with open(self.database_path, 'r') as f:
			datastore = json.load(f)
			datastore[entity.unique_id] = entity.data

		# update db to contain new org's data
		with open(self.database_path, 'w') as f:
			f.write(json.dumps(datastore, indent=4))

	def read_database_path(self, path:list):
		"""Reads data within database path
		path: list of str, as ["path", "to", "data"]"""
		with open(self.database_path, 'r') as f:	
			datastore = json.load(f)
			return self.get_dict_by_path(datastore, path)

	def write_to_database_path(self, path:list, value:any):
		"""Writes data to the database path
		path: list of str, formatted as ["path", "to", "data"]"""
		datastore = {}
		with open(self.database_path, 'r') as f:
			datastore = json.load(f)

		with open(self.database_path, 'w') as f:	
			self.set_dict_by_path(datastore, path, value)
			f.write(json.dumps(datastore, indent=4))

	def get_dict_by_path(self, root, items):
		"""Access a nested object in dict by item sequence."""
		return reduce(operator.getitem, items, root)

	def set_dict_by_path(self, root, items, value):
		"""Set a value in a nested object in dict by item sequence."""
		self.get_dict_by_path(root, items[:-1])[items[-1]] = value

	#################### AGENT FUNCTIONS ######################
	
	def create_agent(self, tier: int, data: dict):
		""" Creates an Agent instance in database and on blockchain """
		''' returns Agent instance if succesfull, None otherwise '''
		
		agent = Agent(tier=tier, data=data)
		
		# save Agent details on blockchain
		if self.contract_transact('createNewAgent', (agent.unique_id, agent.data_hash)):
			# save Agent details in database (after succesfully saved them on blockchain)
			self.save_entity_data_to_database(agent)
			return agent

		return None

	def get_agent_blockchain_details(self, agent_address):
		""" Get data of Agent as stored on blockchain """
		return self.contract_call('viewAgentDetails', (agent_address))

	def get_agent_database_details(self, agent_address):
		""" Reads data of Agent from database """
		return self.read_database_path([agent_address])

	def agent_data_integrity(self, agent_address):
		""" Checks whether data of Agent has been tampered with. """
		
		'''By comparing the hash stored in the blockchain with the one resulted from the database.
		returns True if data HAS NOT been tampered with, False otherwise '''

		if not self.contract_call('isAgent', (agent_address)):
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
		self.contract_transact('setAgentDataHash', (agent_address, data_hash))

	#################### ORGANIZATION FUNCTIONS ######################

	def create_organization(self, tier: int, admin_id: str, data: dict):
		""" Creates an Organization instance on blockchain and in the database"""
		org = Organization(tier=tier, admin_id=admin_id, data=data)
		# add Org details to blockchain
		if self.contract_transact('createNewOrganization',(org.unique_id, admin_id, org.data_hash)):
			# save Org details in db
			self.save_entity_data_to_database(org)
			return org
		return None

if __name__ == '__main__':

	interface = ContractDatabaseInterface()
	agent = interface.create_agent(data = {"general":{}})
	print("Interface Agent Details: ")

	print("data_hash "+ agent.data_hash)
	print("unique_id "+agent.unique_id)

	print("Blo0ckchain Agent Details: ")
	print(interface.get_agent_blockchain_details(agent.unique_id))

	print("Database Agent Details: ")
	print(interface.get_agent_database_details(agent.unique_id))

	print("Has Data Been Tampered With?")
	print(interface.agent_data_integrity(agent.unique_id))

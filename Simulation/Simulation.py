import os
import sys
import time
from pprint import pprint

from Interface.Utilities import Utilities
from Interface.Interface import ContractDatabaseInterface

from Interface.Agent import Agent
from Interface.Constants import AccessType

from multiprocessing import Pool

class Simulation:
	
	def __init__(self, contract_address:str=None, 
		agents_no:int=0, orgs_no:int=0, devs_no:int=0, provider_link:str="http://121.45.192.206:8545"):
		''' Either creates a new Contract or loads one from address, 
			then creates a number of agents, orgs and devices '''

		self.orgs = []
		self.devs = []
		self.agents = []

		overall_start = time.time()

		start = time.time()
		if contract_address == None:
			self.interface = ContractDatabaseInterface(provider_link=provider_link)
			end = time.time()
			print("Creating a new contract instance took %.4f seconds." % (end-start))
		else:
			self.interface = ContractDatabaseInterface(contract_address=contract_address, provider_link=provider_link)
			end = time.time()
			print("Loading contract took %.4f seconds." % (end-start))

		overall_end = time.time()

		self.add_agents(agents_no)
		self.add_orgs(orgs_no)
		self.add_devs(devs_no)

		print("Initializing system with: ")
		print(str(agents_no)+" agents, "+str(devs_no)+" devices and "+str(orgs_no)+" organizations")
		print("Took %.4f seconds." % (overall_end-overall_start))

	def add_agents(self, agents_no):
		pool = Pool()
		all_start = time.time()
		for i in range(0, agents_no):
			start = time.time()
			agent = Agent(interface)
			#agent.
			self.agents.append(agent)	
			end = time.time()
			print("\t Creating one agent took %.4f seconds." % (end-start))
		all_end = time.time()
		print("Creating " +str(agents_no)+ " agents took %.4f seconds." % (all_end-all_start))

	def add_orgs(self, orgs_no):
		orgs_start = time.time()
		for i in range(0, orgs_no):
			start = time.time()
			self.orgs.append(self.interface.create_organization(tier=0, admin_id=self.agents[0].unique_id, data={"general":{}}))
			end = time.time()
			print("\t Creating one organization took %.4f seconds." % (end-start))
		orgs_end = time.time()
		print("Creating " +str(orgs_no)+ " organizations took %.4f seconds." % (orgs_end-orgs_start))

	def add_devs(self, devs_no):
		devs_start = time.time()
		for i in range(0, devs_no):
			start = time.time()
			self.devs.append(self.interface.create_device(admin_id=self.agents[0].unique_id, data={"general":{}}))
			end = time.time()
			print("\t Creating one device took %.4f seconds." % (end-start))
		devs_end = time.time()
		print("Creating " +str(devs_no)+ " devices took %.4f seconds." % (devs_end-devs_start))

	@staticmethod
	def generic_simulation():

		interface = ContractDatabaseInterface(contract_address="0x37C6a1af8aF0F9BE45Ae3869FA6510276b06b0fC", provider_link="http://127.0.0.1:8543", time_it=True)

		print("~~~~~~~~~~~~ CREATING AGENT 1 ~~~~~~~~~~~~")
		start = time.time()
		agent1 = Agent(interface, time_it=True)
		end = time.time()
		print("~~~~~~~~~~~~ CREATING AGENT 1 ~~~~~~~~~~~~ took %.4f s \n" % (end-start))

		print("~~~~~~~~~~~~ CREATING AGENT 2 ~~~~~~~~~~~~")
		start = time.time()
		agent2 = Agent(interface, time_it=True)
		end = time.time()
		print("~~~~~~~~~~~~ CREATING AGENT 2 ~~~~~~~~~~~~ took %.4f s \n" % (end-start))

		print("~~~~~~~~~~~~ CREATING AGENT 3 ~~~~~~~~~~~~")
		start = time.time()
		agent3 = Agent(interface, time_it=True)
		end = time.time()
		print("~~~~~~~~~~~~ CREATING AGENT 3 ~~~~~~~~~~~~ took %.4f s \n" % (end-start))

		print("~~~~~~~~~~~~ CHECKING AGENT 1 DATA INTEGRITY ~~~~~~~~~~~~")
		start = time.time()
		agent1.has_data_integrity()
		end = time.time()
		print("~~~~~~~~~~~~ CHECKING AGENT 1 DATA INTEGRITY ~~~~~~~~~~~~ took %.4f s \n" % (end-start))
		
		print("~~~~~~~~~~~~ CHECKING AGENT 2 DATA INTEGRITY ~~~~~~~~~~~~")
		start = time.time()
		agent2.has_data_integrity()
		end = time.time()
		print("~~~~~~~~~~~~ CHECKING AGENT 2 DATA INTEGRITY ~~~~~~~~~~~~ took %.4f s \n" % (end-start))

		print("~~~~~~~~~~~~ CHECKING AGENT 3 DATA INTEGRITY ~~~~~~~~~~~~")
		start = time.time()
		agent3.has_data_integrity()
		end = time.time()
		print("~~~~~~~~~~~~ CHECKING AGENT 3 DATA INTEGRITY ~~~~~~~~~~~~ took %.4f s \n" % (end-start))

		print("~~~~~~~~~~~~ GIVE AGENT 2 ADMIN ACCESS TO AGENT 1's DATA ~~~~~~~~~~~~")
		start = time.time()
		agent1.give_agent_access_to_data(agent2.unique_id, AccessType.ADMIN, "data_1")
		end = time.time()
		print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ took %.4f s \n" % (end-start))

		print("~~~~~~~~~~~~ GIVE AGENT 3 ADMIN ACCESS TO AGENT 1's DATA ~~~~~~~~~~~~")
		start = time.time()
		agent1.give_agent_access_to_data(agent3.unique_id, AccessType.ADMIN, "data_1")
		end = time.time()
		print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ took %.4f s \n" % (end-start))


		print("~~~~~~~~~~~~ GIVE AGENT 1 ADMIN ACCESS TO AGENT 2's DATA ~~~~~~~~~~~~")
		start = time.time()
		agent2.give_agent_access_to_data(agent1.unique_id, AccessType.ADMIN, "data_2")
		end = time.time()
		print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ took %.4f s \n" % (end-start))


		print("~~~~~~~~~~~~ GIVE AGENT 3 ADMIN ACCESS TO AGENT 2's DATA ~~~~~~~~~~~~")
		start = time.time()
		agent2.give_agent_access_to_data(agent3.unique_id, AccessType.ADMIN, "data_2")
		end = time.time()
		print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ took %.4f s \n" % (end-start))


		# agent1.get_agent_access_rights_to_data(agent2.unique_id, "data_1")
		# agent1.get_agent_access_rights_to_data(agent3.unique_id, "data_1")
		# agent2.get_agent_access_rights_to_data(agent1.unique_id, "data_2")
		# agent2.get_agent_access_rights_to_data(agent3.unique_id, "data_2")

		try:
			while True:
				print("~~~~~~~~~~~~ AGENT 2 IS WRITING TO AGENT 1's DATA ~~~~~~~~~~~~")
				start = time.time()
				agent2.write_to_agent_data_path(path=["data_1", "subfolder_1"], value={"succesful_written_by":agent2.unique_id}, owner_id=agent1.unique_id)
				end = time.time()
				print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ took %.4f s \n" % (end-start))

				
				print("~~~~~~~~~~~~ AGENT 3 IS READING FROM AGENT 1's DATA ~~~~~~~~~~~~")
				start = time.time()
				agent3.read_agent_data_path(path=["data_1", "subfolder_1"], owner_id=agent1.unique_id)
				end = time.time()
				print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ took %.4f s \n" % (end-start))


				print("~~~~~~~~~~~~ AGENT 1 IS WRITING TO AGENT 2's DATA ~~~~~~~~~~~~")
				start = time.time()
				agent1.write_to_agent_data_path(path=["data_2", "subfolder_1"], value={"succesful_written_by":agent1.unique_id}, owner_id=agent2.unique_id)
				end = time.time()
				print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ took %.4f s \n" % (end-start))

				print("~~~~~~~~~~~~ AGENT 3 IS READING FROM AGENT 2's DATA ~~~~~~~~~~~~")
				start = time.time()
				agent3.read_agent_data_path(path=["data_2", "subfolder_1"], owner_id=agent2.unique_id)
				end = time.time()
				print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ took %.4f s \n" % (end-start))

		except KeyboardInterrupt:
			print("Quitting ... ")


		print("~~~~~~~~~~~~ CHECKING AGENT 1's DATA INTEGRITY ~~~~~~~~~~~~")
		start = time.time()
		print("Has data integrity? "+agent1.has_data_integrity())
		end = time.time()
		print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ took %.4f s \n" % (end-start))

		print("~~~~~~~~~~~~ CHECKING AGENT 2's DATA INTEGRITY ~~~~~~~~~~~~")
		start = time.time()
		print("Has data integrity? "+agent2.has_data_integrity())
		end = time.time()
		print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ took %.4f s \n" % (end-start))

		print("~~~~~~~~~~~~ CHECKING AGENT 3's DATA INTEGRITY ~~~~~~~~~~~~")
		start = time.time()
		print("Has data integrity? "+agent3.has_data_integrity())
		end = time.time()
		print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ took %.4f s \n" % (end-start))

	@staticmethod
	def time_function(func:any, args:tuple=()):
		''' Times how long it takes to run a function '''
		start = time.time()
		something = func(*args)
		end = time.time()
		return (end-start)

	@staticmethod
	def time_create_interface_with_new_contract():
		''' Times how long it takes to create an interface by instantianing a new smart contract '''
		time = time_function(func=ContractDatabaseInterface)
		print("Creating interface from new contract took %.4f seconds." % (time))

	@staticmethod
	def time_creating_agent():
		''' Times how long it takes to create a new Agent '''
		start = time.time()
		interface = ContractDatabaseInterface(contract_address="0xdc6958B5065c95473e1BbfC72278F00a21E27E23")
		end = time.time()
		print("Loading interface from address took %.4f seconds." % (end-start))

		result_time = time_function(func=interface.create_agent, args=(0, {"general":{ "more" : { "agents": { "0x88a455CDCa7B636993d518e2FbA0E37DD8F5fc63": { "general": {  "fname": "The Imp", "lname": "Lannister", "public_key": "0xf9fa3d5c7ee62258fbd83a1f6a0b303526a0eb86abfcb918b8069acad55cb61ba824fe66a68adfa220e86f710242c515fd63465d0898711d13765173f65eb728", "tier": 3, "unique_id": "0x88a455CDCa7B636993d518e2FbA0E37DD8F5fc63" } }, "0x013cFEc6BD977Ec5A86770646bE00880e356B313": { "general": { "fname": "Sansa", "lname": "Lannister", "public_key": "0x90d412aa6d14fba6cf7af08b46fb98a5e747b3e745b653a238f88ab28c31ae1603af9afd12781033f3b1b90598500cb674cbaddbc1bdfe58b27fa0243816f7d6", "tier": 3, "unique_id": "0x013cFEc6BD977Ec5A86770646bE00880e356B313" } }, "0xd40Ba8aA9354e1218827A0d6f93E0e02E01974F7": { "general": { "fname": "Tyrion", "lname": "Lannister", "public_key": "0xdec5c4d8b71c4ceffdf86bdf926c6b3b22fd5f2c95db11b379be8db688cb9f281b3f042a2ce00d22cdd0d4b9abf4ce9a5e5dea3ed579088ac1ceb1bad12df911", "tier": 3, "unique_id": "0xd40Ba8aA9354e1218827A0d6f93E0e02E01974F7"}}},"organizations": {},"devices": {}}}}))
		print("Creating an agent took %.4f seconds." % (result_time))

	@staticmethod
	def test_blockchain_integrity_scenario():
		''' Times an integrity scenario and tests the integrity of the interface
		By changing the data from the DB without blockchain validation and then 
		validates it '''

		overall_start = time.time()

		start = time.time()
		interface = ContractDatabaseInterface(contract_address="0xc3eB615865B9892a7Cb9AdD480cbB0Df1D31B32d")
		end = time.time()
		print("Loading interface from address took %.4f seconds." % (end-start))

		### Create an agent, then check database and blockchain data, then check integrity
		start = time.time()
		agent = interface.create_agent(tier=3, data={"general":{"fname":"Tyrion", "lname":"Lannister"}})
		end = time.time()
		print("Creating agent took %.4f seconds." % (end-start))

		start = time.time()
		assert interface.agent_data_integrity(agent.unique_id) == True 
		end = time.time()
		print("Checking agent's data integrity took %.4f seconds." % (end-start))

		### Change agent data in database without changing blockchain, then check data integrity
		start = time.time()
		interface.write_to_database_path(['agents', agent.unique_id, 'general', 'fname'], "The Imp")
		end = time.time()
		print("Changing agent's data in db took %.4f seconds." % (end-start))


		start = time.time()
		assert interface.agent_data_integrity(agent.unique_id) == False 
		end = time.time()
		print("Checking agent's data integrity (again) took %.4f seconds." % (end-start))

		### Change data_hash in blockchain to match the actual hash of database

		start = time.time()
		interface.validate_agent_data_on_blockchain(agent.unique_id)
		end = time.time()
		print("Validating agent's new data on blockchain took %.4f seconds." % (end-start))

		start = time.time()
		assert interface.agent_data_integrity(agent.unique_id) == True 
		end = time.time()
		print("Checking agent's data integrity (again) took %.4f seconds." % (end-start))

		overall_end = time.time()

		print("In total, this took %.4f seconds." % (overall_end-overall_start))

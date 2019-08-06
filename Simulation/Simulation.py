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
		agents_no:int=0, orgs_no:int=0, devs_no:int=0, provider_link:str="http://103.217.166.130:8540"):
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
	def generic_simulation(acct_address=None, acct_pass=""):
		''' 
			Runs a generic simulation involving 6 entities reading and writing data to and from each other. 
			Run this on 15 separate nodes and you're simulating a system with 90 entities interacting on the blockchain.
 
			Compute the average amount of time it takes for a function on the blockchain to be computed .
		'''

		interface = ContractDatabaseInterface(contract_address="0xfae92c423740318ba144db41328a7580871319d2", provider_link="http://127.0.0.1:8540", time_it=True, default_acct_address=acct_address, default_acct_pass=acct_pass)

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

		print("~~~~~~~~~~~~ CREATING AGENT 4 ~~~~~~~~~~~~")
		start = time.time()
		agent4 = Agent(interface, time_it=True)
		end = time.time()
		print("~~~~~~~~~~~~ CREATING AGENT 4 ~~~~~~~~~~~~ took %.4f s \n" % (end-start))

		print("~~~~~~~~~~~~ CREATING AGENT 5 ~~~~~~~~~~~~")
		start = time.time()
		agent5 = Agent(interface, time_it=True)
		end = time.time()
		print("~~~~~~~~~~~~ CREATING AGENT 5 ~~~~~~~~~~~~ took %.4f s \n" % (end-start))

		print("~~~~~~~~~~~~ CREATING AGENT 6 ~~~~~~~~~~~~")
		start = time.time()
		agent6 = Agent(interface, time_it=True)
		end = time.time()
		print("~~~~~~~~~~~~ CREATING AGENT 6 ~~~~~~~~~~~~ took %.4f s \n" % (end-start))

		print("\n\n~~~~~~~~~~~~ Now Wait 11 seconds for the blocks to mine ~~~~~~~~~~~~\n\n")
		time.sleep(11)

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



		print("~~~~~~~~~~~~ GIVE AGENT 5 ADMIN ACCESS TO AGENT 4's DATA ~~~~~~~~~~~~")
		start = time.time()
		agent4.give_agent_access_to_data(agent5.unique_id, AccessType.ADMIN, "data_1")
		end = time.time()
		print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ took %.4f s \n" % (end-start))

		print("~~~~~~~~~~~~ GIVE AGENT 6 ADMIN ACCESS TO AGENT 4's DATA ~~~~~~~~~~~~")
		start = time.time()
		agent4.give_agent_access_to_data(agent6.unique_id, AccessType.ADMIN, "data_1")
		end = time.time()
		print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ took %.4f s \n" % (end-start))


		print("~~~~~~~~~~~~ GIVE AGENT 4 ADMIN ACCESS TO AGENT 5's DATA ~~~~~~~~~~~~")
		start = time.time()
		agent5.give_agent_access_to_data(agent4.unique_id, AccessType.ADMIN, "data_2")
		end = time.time()
		print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ took %.4f s \n" % (end-start))


		print("~~~~~~~~~~~~ GIVE AGENT 6 ADMIN ACCESS TO AGENT 5's DATA ~~~~~~~~~~~~")
		start = time.time()
		agent6.give_agent_access_to_data(agent6.unique_id, AccessType.ADMIN, "data_2")
		end = time.time()
		print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ took %.4f s \n" % (end-start))

		# agent1.get_agent_access_rights_to_data(agent2.unique_id, "data_1")
		# agent1.get_agent_access_rights_to_data(agent3.unique_id, "data_1")
		# agent2.get_agent_access_rights_to_data(agent1.unique_id, "data_2")
		# agent2.get_agent_access_rights_to_data(agent3.unique_id, "data_2")
		
		print("\n\n~~~~~~~~~~~~ Now Wait 11 seconds for the blocks to mine ~~~~~~~~~~~~\n\n")
		time.sleep(11)

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


				print("~~~~~~~~~~~~ AGENT 5 IS WRITING TO AGENT 4's DATA ~~~~~~~~~~~~")
				start = time.time()
				agent5.write_to_agent_data_path(path=["data_1", "subfolder_1"], value={"succesful_written_by":agent5.unique_id}, owner_id=agent4.unique_id)
				end = time.time()
				print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ took %.4f s \n" % (end-start))

				
				print("~~~~~~~~~~~~ AGENT 6 IS READING FROM AGENT 4's DATA ~~~~~~~~~~~~")
				start = time.time()
				agent6.read_agent_data_path(path=["data_1", "subfolder_1"], owner_id=agent4.unique_id)
				end = time.time()
				print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ took %.4f s \n" % (end-start))


				print("~~~~~~~~~~~~ AGENT 4 IS WRITING TO AGENT 5's DATA ~~~~~~~~~~~~")
				start = time.time()
				agent4.write_to_agent_data_path(path=["data_2", "subfolder_1"], value={"succesful_written_by":agent4.unique_id}, owner_id=agent5.unique_id)
				end = time.time()
				print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ took %.4f s \n" % (end-start))

				print("~~~~~~~~~~~~ AGENT 6 IS READING FROM AGENT 5's DATA ~~~~~~~~~~~~")
				start = time.time()
				agent6.read_agent_data_path(path=["data_2", "subfolder_1"], owner_id=agent5.unique_id)
				end = time.time()
				print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ took %.4f s \n" % (end-start))

		except KeyboardInterrupt:
			print("Quitting ... ")


		print("~~~~~~~~~~~~ CHECKING AGENT 1's DATA INTEGRITY ~~~~~~~~~~~~")
		start = time.time()
		print("Has data integrity? "+str(agent1.has_data_integrity()))
		end = time.time()
		print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ took %.4f s \n" % (end-start))

		print("~~~~~~~~~~~~ CHECKING AGENT 2's DATA INTEGRITY ~~~~~~~~~~~~")
		start = time.time()
		print("Has data integrity? "+str(agent2.has_data_integrity()))
		end = time.time()
		print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ took %.4f s \n" % (end-start))

		print("~~~~~~~~~~~~ CHECKING AGENT 3's DATA INTEGRITY ~~~~~~~~~~~~")
		start = time.time()
		print("Has data integrity? "+str(agent3.has_data_integrity()))
		end = time.time()
		print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ took %.4f s \n" % (end-start))


		print("~~~~~~~~~~~~ CHECKING AGENT 4's DATA INTEGRITY ~~~~~~~~~~~~")
		start = time.time()
		print("Has data integrity? "+str(agent4.has_data_integrity()))
		end = time.time()
		print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ took %.4f s \n" % (end-start))

		print("~~~~~~~~~~~~ CHECKING AGENT 5's DATA INTEGRITY ~~~~~~~~~~~~")
		start = time.time()
		print("Has data integrity? "+str(agent5.has_data_integrity()))
		end = time.time()
		print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ took %.4f s \n" % (end-start))

		print("~~~~~~~~~~~~ CHECKING AGENT 6's DATA INTEGRITY ~~~~~~~~~~~~")
		start = time.time()
		print("Has data integrity? "+str(agent6.has_data_integrity()))
		end = time.time()
		print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ took %.4f s \n" % (end-start))


	@staticmethod
	def tps_simulation(acct_address=None, acct_pass="", provider_link="http://127.0.0.1:8538"):
		''' 
			Runs a generic simulation involving 6 entities reading and writing data to and from each other. 
			Run this on 15 separate nodes and you're simulating a system with 90 entities interacting on the blockchain.
 
			Compute the average amount of time it takes for a function on the blockchain to be computed .
		'''

		sim_start = time.time()
		total_txs = 0

		interface = ContractDatabaseInterface(contract_address="0x594ec95ce0ad3222bc569019577fb29d85793352", provider_link=provider_link, time_it=True, default_acct_address=acct_address, default_acct_pass=acct_pass)

		print("~~~~~~~~~~~~ CREATING AGENT 1 ~~~~~~~~~~~~")
		start = time.time()
		agent1 = Agent(interface, time_it=True, await_receipt=False)
		total_txs = total_txs + 2
		end = time.time()
		print("~~~~~~~~~~~~ CREATING AGENT 1 ~~~~~~~~~~~~ took %.4f s \n" % (end-start))

		print("~~~~~~~~~~~~ CREATING AGENT 2 ~~~~~~~~~~~~")
		start = time.time()
		agent2 = Agent(interface, time_it=True, await_receipt=False)
		total_txs = total_txs + 2
		end = time.time()
		print("~~~~~~~~~~~~ CREATING AGENT 2 ~~~~~~~~~~~~ took %.4f s \n" % (end-start))

		print("~~~~~~~~~~~~ CREATING AGENT 3 ~~~~~~~~~~~~")
		start = time.time()
		agent3 = Agent(interface, time_it=True, await_receipt=False)
		total_txs = total_txs + 2
		end = time.time()
		print("~~~~~~~~~~~~ CREATING AGENT 3 ~~~~~~~~~~~~ took %.4f s \n" % (end-start))

		print("~~~~~~~~~~~~ CREATING AGENT 4 ~~~~~~~~~~~~")
		start = time.time()
		agent4 = Agent(interface, time_it=True, await_receipt=False)
		total_txs = total_txs + 2
		end = time.time()
		print("~~~~~~~~~~~~ CREATING AGENT 4 ~~~~~~~~~~~~ took %.4f s \n" % (end-start))

		print("~~~~~~~~~~~~ CREATING AGENT 5 ~~~~~~~~~~~~")
		start = time.time()
		agent5 = Agent(interface, time_it=True, await_receipt=False)
		total_txs = total_txs + 2
		end = time.time()
		print("~~~~~~~~~~~~ CREATING AGENT 5 ~~~~~~~~~~~~ took %.4f s \n" % (end-start))

		print("~~~~~~~~~~~~ CREATING AGENT 6 ~~~~~~~~~~~~")
		start = time.time()
		agent6 = Agent(interface, time_it=True, await_receipt=False)
		total_txs = total_txs + 2
		end = time.time()
		print("~~~~~~~~~~~~ CREATING AGENT 6 ~~~~~~~~~~~~ took %.4f s \n" % (end-start))

		print("~~~~~~~~~~~~ CREATING AGENT 7 ~~~~~~~~~~~~")
		start = time.time()
		agent7 = Agent(interface, time_it=True, await_receipt=False)
		total_txs = total_txs + 2
		end = time.time()
		print("~~~~~~~~~~~~ CREATING AGENT 7 ~~~~~~~~~~~~ took %.4f s \n" % (end-start))

		print("~~~~~~~~~~~~ CREATING AGENT 8 ~~~~~~~~~~~~")
		start = time.time()
		agent8 = Agent(interface, time_it=True, await_receipt=False)
		total_txs = total_txs + 2
		end = time.time()
		print("~~~~~~~~~~~~ CREATING AGENT 8 ~~~~~~~~~~~~ took %.4f s \n" % (end-start))

		print("~~~~~~~~~~~~ CREATING AGENT 9 ~~~~~~~~~~~~")
		start = time.time()
		agent9 = Agent(interface, time_it=True, await_receipt=False)
		total_txs = total_txs + 2
		end = time.time()
		print("~~~~~~~~~~~~ CREATING AGENT 9 ~~~~~~~~~~~~ took %.4f s \n" % (end-start))

		print("\n\n~~~~~~~~~~~~ Now Wait a few seconds for the blocks to mine ~~~~~~~~~~~~\n\n")
		time.sleep(5)

		print("\n\n~~~~~~~~~~~~ Now We start writing to the blockchain, press CTRL+C to get to next step ~~~~~~~~~~~~\n\n")
		try:
			i = 0
			while True:
				agent1.give_agent_access_to_data(agent2.unique_id, AccessType.ADMIN, "data_"+str(i), await_receipt=False)
				agent1.give_agent_access_to_data(agent3.unique_id, AccessType.ADMIN, "data_"+str(i), await_receipt=False)
				agent2.give_agent_access_to_data(agent1.unique_id, AccessType.READ, "data_"+str(i), await_receipt=False)
				agent2.give_agent_access_to_data(agent3.unique_id, AccessType.WRITE, "data_"+str(i), await_receipt=False)

				agent4.give_agent_access_to_data(agent5.unique_id, AccessType.ADMIN, "data_"+str(i), await_receipt=False)
				agent4.give_agent_access_to_data(agent6.unique_id, AccessType.ADMIN, "data_"+str(i), await_receipt=False)
				agent5.give_agent_access_to_data(agent4.unique_id, AccessType.READ, "data_"+str(i), await_receipt=False)
				agent5.give_agent_access_to_data(agent6.unique_id, AccessType.WRITE, "data_"+str(i), await_receipt=False)

				agent7.give_agent_access_to_data(agent8.unique_id, AccessType.ADMIN, "data_"+str(i), await_receipt=False)
				agent7.give_agent_access_to_data(agent9.unique_id, AccessType.ADMIN, "data_"+str(i), await_receipt=False)
				agent8.give_agent_access_to_data(agent7.unique_id, AccessType.READ, "data_"+str(i), await_receipt=False)
				agent8.give_agent_access_to_data(agent9.unique_id, AccessType.WRITE, "data_"+str(i), await_receipt=False)

				i = i + 1
				print(str(i))
				total_txs = total_txs + 12

		except KeyboardInterrupt:
			print("Quitting ... ")
		
		print("\n\n~~~~~~~~~~~~ Now Wait a few seconds for the blocks to mine, before we check the blockchain for mistakes ~~~~~~~~~~~~\n\n")
		time.sleep(13)

		incorrect = 0
		
		for j in range(0, i):
			access_right = agent1.get_agent_access_rights_to_data(accessor_id=agent2.unique_id, data_path="data_"+str(j))
			if access_right != 3:
				print("access right of agent 2 to agent 1's path \'"+"data_"+str(j) +"\'' seems to be wrong, should be "+str(3)+", but is "+str(access_right))
				incorrect = incorrect + 1
			access_right = agent1.get_agent_access_rights_to_data(accessor_id=agent3.unique_id, data_path="data_"+str(j))
			if access_right != 3:
				print("access right of agent 3 to agent 1's path \'"+"data_"+str(j) +"\'' seems to be wrong, should be "+str(3)+", but is "+str(access_right))
				incorrect = incorrect + 1

			access_right = agent2.get_agent_access_rights_to_data(accessor_id=agent1.unique_id, data_path="data_"+str(j))
			if access_right != 1:
				print("access right of agent 1 to agent 2's path \'"+"data_"+str(j) +"\'' seems to be wrong, should be "+str(1)+", but is "+str(access_right))
				incorrect = incorrect + 1
			access_right = agent2.get_agent_access_rights_to_data(accessor_id=agent3.unique_id, data_path="data_"+str(j))
			if access_right != 2:
				print("access right of agent 3 to agent 2's path \'"+"data_"+str(j) +"\'' seems to be wrong, should be "+str(2)+", but is "+str(access_right))
				incorrect = incorrect + 1

			access_right = agent4.get_agent_access_rights_to_data(accessor_id=agent5.unique_id, data_path="data_"+str(j))
			if access_right != 3:
				print("access right of agent 2 to agent 1's path \'"+"data_"+str(j) +"\'' seems to be wrong, should be "+str(3)+", but is "+str(access_right))
				incorrect = incorrect + 1
			access_right = agent4.get_agent_access_rights_to_data(accessor_id=agent6.unique_id, data_path="data_"+str(j))
			if access_right != 3:
				print("access right of agent 3 to agent 1's path \'"+"data_"+str(j) +"\'' seems to be wrong, should be "+str(3)+", but is "+str(access_right))
				incorrect = incorrect + 1

			access_right = agent5.get_agent_access_rights_to_data(accessor_id=agent4.unique_id, data_path="data_"+str(j))
			if access_right != 1:
				print("access right of agent 1 to agent 2's path \'"+"data_"+str(j) +"\'' seems to be wrong, should be "+str(1)+", but is "+str(access_right))
				incorrect = incorrect + 1
			access_right = agent5.get_agent_access_rights_to_data(accessor_id=agent6.unique_id, data_path="data_"+str(j))
			if access_right != 2:
				print("access right of agent 3 to agent 2's path \'"+"data_"+str(j) +"\'' seems to be wrong, should be "+str(2)+", but is "+str(access_right))
				incorrect = incorrect + 1

			access_right = agent7.get_agent_access_rights_to_data(accessor_id=agent8.unique_id, data_path="data_"+str(j))
			if access_right != 3:
				print("access right of agent 2 to agent 1's path \'"+"data_"+str(j) +"\'' seems to be wrong, should be "+str(3)+", but is "+str(access_right))
				incorrect = incorrect + 1
			access_right = agent7.get_agent_access_rights_to_data(accessor_id=agent9.unique_id, data_path="data_"+str(j))
			if access_right != 3:
				print("access right of agent 3 to agent 1's path \'"+"data_"+str(j) +"\'' seems to be wrong, should be "+str(3)+", but is "+str(access_right))
				incorrect = incorrect + 1

			access_right = agent8.get_agent_access_rights_to_data(accessor_id=agent7.unique_id, data_path="data_"+str(j))
			if access_right != 1:
				print("access right of agent 1 to agent 2's path \'"+"data_"+str(j) +"\'' seems to be wrong, should be "+str(1)+", but is "+str(access_right))
				incorrect = incorrect + 1
			access_right = agent8.get_agent_access_rights_to_data(accessor_id=agent9.unique_id, data_path="data_"+str(j))
			if access_right != 2:
				print("access right of agent 3 to agent 2's path \'"+"data_"+str(j) +"\'' seems to be wrong, should be "+str(2)+", but is "+str(access_right))
				incorrect = incorrect + 1


		if incorrect == 0:
			print("Congrats! No incorrect writes on the blockchain! ")
		else:
			print("There were "+str(incorrect)+" incorrect writes on the blockchain, out of "+str(i*4))

		sim_stop = time.time()
		print("The whole simulation took "+str(int(sim_stop-sim_start))+"s")
		print("This node alone generated "+str(total_txs)+" transactions")

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

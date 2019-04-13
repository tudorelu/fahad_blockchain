'''
Written by Tudor Barbulescu. 

Interface used to interact with smart contracts on the blockchain.

Kudos to Nick for Inspiration:
https://hackernoon.com/ethereum-smart-contracts-in-python-a-comprehensive-ish-guide-771b03990988
'''

import time
from web3 import Web3, HTTPProvider

# need to generate the abi derived from the contract itself
import contract_abi

''' 
	This class defines an interface which enables the interaction between an 
	ethereum smart contract and a locally stored SQL database. 

	The smart contract acts as an authentication layer on top of the database, 
	providing the access rights for Entiies to read and write to the database.

	The interface connects to the smart contract by using web3.py and to the
	database through the sqlite3 library.

	The database contains general information about th Entities involved in 
	the system. An Entity can either be an Individual (Agent) or an Organiza-
	tion. Entities should not have access to the entire database, instead they
	should only be allowed to access specific parts. These parts are defined 
	by the ACCESS RIGHTS module, which will probably be another database.

'''
class ContractDatabaseInterface:

	def __init__(self):

		# address of contract we'll be interacting with 
		self.contract_address     = [YOUR CONTRACT ADDRESS]

		# private key of user who's interacting with contract
		self.wallet_private_key   = [YOUR TEST WALLET PRIVATE KEY]
		
		# address of user who'se interacting with contract
		self.wallet_address       = [YOUR WALLET ADDRESS]

		# web3 provider
		self.w3 = Web3(HTTPProvider([YOUR INFURA URL]))
		
		# contract that the user will be interacting with
		self.contract = self.w3.eth.contract(address = self.contract_address, abi = contract_abi.abi)

		# enables unaudited features of web3
		#self.w3.eth.enable_unaudited_features()

	def send_ether_to_contract(self, amount_in_ether):

		# amount (in wei) to send to the contract, derived from ether amount (10^18 wei = 1 ether)
	    amount_in_wei = self.w3.toWei(amount_in_ether,'ether');

	    # generate nonce (tx c)
	    nonce = self.w3.eth.getTransactionCount(self.wallet_address)

	    # transaction information
	    txn_dict = {
	            'to': self.contract_address,
	            'value': amount_in_wei,
	            'gas': 2000000,
	            'gasPrice': w3.toWei('40', 'gwei'),
	            'nonce': nonce,
	            'chainId': 3		# chainId = 1 for main net, 3 for ropsten, 42 for kovan; 
	            					# check https://github.com/ethereumbook/ethereumbook/issues/110
	    }

	    # generate signed tx
	    signed_txn = self.w3.eth.account.signTransaction(txn_dict, self.wallet_private_key)
	    
	    # send tx and get tx hash (to check whether tx has been received)
	    txn_hash = self.w3.eth.sendRawTransaction(signed_txn.rawTransaction)

	    txn_receipt = None
	    count = 0

	    # check if the tx was received by the blockchain
	    while txn_receipt is None and (count < 30):
	        txn_receipt = w3.eth.getTransactionReceipt(txn_hash)
	        print(txn_receipt)
	        time.sleep(10)

	    # if it hasn't been received within 300 seconds, it means the transaction failed
	    if txn_receipt is None:
	        return {'status': 'failed', 'error': 'timeout'}
	    # otherwise, it was added
	    return {'status': 'added', 'txn_receipt': txn_receipt}

	'''	this is how a contract function call looks like	'''
    def call_contract_function(self, function_name, params):
	    return self.contract.functions.function_name(params).call()
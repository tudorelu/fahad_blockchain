# Installation Prerequisites

## SYSTEM
[python3]()

[ethereum]()

[solidity]()

ganache [ui]() or [cli]()

## PYTHON3 

First install the [pip3]() package manager, to be able to install the other useful packages.

Web3 (Interface Connecting to ETH network )
```py
pip install web3
```

Solidity Compiler
```py
pip install py_solcx
```

Ethereum Key Utilities
```py
pip install eth_keys
pip install eth_utils
```

Ellyptic Curve Cryptography for Wallet Generation
```py
pip install py_ecies
```

Library for Hashing Data
```py
pip install hashlib
```
# Commands for Testing the functionality of the Interface

To test the ContractDatabaseInterface, start Ganache and run python3 from within the Interface folder

After starting Ganache:

```sh
cd Interface
python3

```

```py

from pprint import pprint
from Utilities import Utilities
from ContractDatabaseInterface import ContractDatabaseInterface

interface = ContractDatabaseInterface()

```

## TEST DATA INTEGRITY

```py

### Create an agent, then check database and blockchain data, then check integrity

agent = interface.create_agent(tier=3, data={"general":{"fname":"Tyrion", "lname":"Lannister"}})

pprint(interface.get_agent_database_details(agent.unique_id))
pprint(interface.get_agent_blockchain_details(agent.unique_id))

interface.agent_data_integrity(agent.unique_id) ## Should Return True

```

```py

### Change agent data in database without changing blockchain, then check data integrity

interface.write_to_database_path([agent.unique_id, 'general', 'fname'], "Kingslayer")

pprint(interface.get_agent_database_details(agent.unique_id))
pprint(Utilities.hash_data(interface.get_agent_database_details(agent.unique_id)))
pprint(interface.get_agent_blockchain_details(agent.unique_id))

interface.agent_data_integrity(agent.unique_id) ## Should Return False

```

```py

### Change data_hash in blockchain to match the actual hash of database

interface.validate_agent_data_on_blockchain(agent.unique_id)

interface.agent_data_integrity(agent.unique_id) ## Should Return True

```

```py

### Create organization

org = interface.create_organization(tier=5, admin_id=agent.unique_id, data={"general":{"name":"University Hospital", "address":"Rue de la Versaille, London, Paris"}})

```


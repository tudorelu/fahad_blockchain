# Installation Prerequisites

## SYSTEM
[python >= 3.6](http://lmgtfy.com/?q=install+python3)

[ethereum & geth](https://github.com/ethereum/go-ethereum/wiki/Building-Ethereum)

[solidity compiler](https://solidity.readthedocs.io/en/v0.5.3/installing-solidity.html#binary-packages)


## PYTHON3 

First install the pip3 ([ubuntu](https://linuxize.com/post/how-to-install-pip-on-ubuntu-18.04/), [mac](https://evansdianga.com/install-pip-osx/) or [windows](http://lmgtfy.com/?q=install+pip3+on+windows)) package manager, in order to be able to install the other useful packages.

Web3 (Interface Connecting to ETH network )
```py
pip3 install web3
```

Solidity Compiler
```py
pip3 install py_solcx
```

Ethereum Key Utilities
```py
pip3 install eth_keys
pip3 install eth_utils
```

Ellyptic Curve Cryptography for Wallet Generation
```py
pip3 install eciespy
```

Library for Hashing Data
```py
pip3 install hashlib
```
# Commands for Testing the functionality of the Interface

To test the ContractDatabaseInterface, start Ganache, or your own provider and run python3 from within the root folder

After starting Ganache:

```sh
cd Interface
python3

```

```py

from pprint import pprint
from Interface.Utilities import Utilities
from Interface.Interface import ContractDatabaseInterface

interface = ContractDatabaseInterface()

```

## TEST DATA INTEGRITY

```py

from pprint import pprint
from Interface.Utilities import Utilities
from Interface.Interface import ContractDatabaseInterface

interface = ContractDatabaseInterface()

### Create an agent, then check database and blockchain data, then check integrity

agent = Agent(interface=interface,tier=3, data={"general":{"fname":"Mister", "lname":"Tyrell"}})

pprint(agent.get_database_details())
pprint(agent.get_blockchain_details())

agent.has_data_integrity() ## Should Return True

```

```py

### Change agent data in database without changing blockchain, then check data integrity

interface.write_to_database_path(['agents', agent.unique_id, 'general', 'fname'], "The Imp")

pprint(agent.get_database_details())
pprint(Utilities.hash_data(agent.get_database_details()))
pprint(agent.get_blockchain_details())

agent.has_data_integrity() ## Should Return False

```

```py

### Change data_hash in blockchain to match the actual hash of database

interface.validate_agent_data_on_blockchain(agent.unique_id)

interface.agent_data_integrity(agent.unique_id) ## Should Return True

```

```py

### Create organization

org = interface.create_organization(tier=5, admin_id=agent.unique_id, data={"general":{"name":"House Lannister", "symbol":"Lion", "address":"King's Landing"}})

```

## TEST ACCESS RIGHTS

```py

```

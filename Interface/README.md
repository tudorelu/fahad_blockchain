# Commands for Testing the functionality of the Interface

To test the ContractDatabaseInterface, start Ganache, or your own provider and run python3 from within the root folder

After starting Ganache:

```sh
cd Interface
python3

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

agent.validate_data_on_blockchain()

agent.has_data_integrity() ## Should Return True

```

```py

### Create organization

org = interface.create_organization(tier=5, admin_id=agent.unique_id, data={"general":{"name":"House Lannister", "symbol":"Lion", "address":"King's Landing"}})

```

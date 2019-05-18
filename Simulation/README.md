## Simulation Plan

#### Initialization Script

	*	Creates or connects to an instance of the contract
	*	If creating new instance, add a number of entities
	*	For each entity give it access to other entities' data

#### Simulation For Individual Nodes

	*	Connects to the private blockchain we created
	*	Authenticates as an Agent / Organization
	*	Randomly access and change data of entities  
	*	Time the accessing and changing of data

#### Simulation For The Whole Network
	
	*	Run the individual nodes simulation from multiple computers (aws)


```sh

interface.give_agent_access_to_another_agent_data(agent1.unique_id, agent2.unique_id, AccessType.WRITE, "data_1/subfolder_1")
```

```py

from Interface.Agent import Agent
from Interface.Interface import ContractDatabaseInterface
from Interface.Constants import AccessType

interface = ContractDatabaseInterface(contract_address="0x37C6a1af8aF0F9BE45Ae3869FA6510276b06b0fC", provider_link="http://127.0.0.1:8543")

agent1 = Agent(interface)
agent2 = Agent(interface)

agent1.has_data_integrity()
agent2.has_data_integrity()

agent1.give_agent_access_to_data(agent2.unique_id, AccessType.ADMIN, "data_1")

agent1.get_agent_access_rights_to_data(agent2.unique_id, "data_1")

agent2.write_to_agent_data_path(path=["data_1", "subfolder_1"], value={"succesful_written_by":agent2.unique_id}, owner_id=agent1.unique_id)

agent1.has_data_integrity()
agent2.has_data_integrity()


```
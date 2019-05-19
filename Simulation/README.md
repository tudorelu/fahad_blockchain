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


```py

from Simulation.Simulation import Simulation

Simulation.generic_simulation()

```

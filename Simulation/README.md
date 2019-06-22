# Simulation Plan

This script is used to run different kinds of tests on the system, like timing certain actions, checking the integrity after changing some data within the db, or running a generic simulation that times the interaction between 6 entities.

### Initialization Script

	*	Creates or connects to an instance of the contract
	*	If creating new instance, add a number of entities 
	*	For each entity give it access to other entities' data

### Simulation For Individual Nodes

	*	Connects to the private blockchain we created
	*	Authenticates as an Agent / Organization
	*	Randomly access and change data between entities 
	*	Time the accessing and changing of data

#### Simulation For The Whole Network

	*	Run the individual nodes simulation from multiple computers (AWS)

```py

from Simulation.Simulation import Simulation

Simulation.generic_simulation()

```
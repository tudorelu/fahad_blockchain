# Running a Private Blockchain

Using ```parity```, we're running a private Proof of Authority network on top of which we run our smart contract.

The starting point for running a private networks comes from parity's [Demo PoA tutorial](https://github.com/tudorelu/wiki/blob/master/Demo-PoA-tutorial.md)

## Initializing Nodes
### On Initial Computer
#### Node 0
#### Optional Node 1

### On Subsequent Computers
#### Step 0

Please make sure that the remote nodes are on the same time zone as the initial node, and that the times match.

On an Ubuntu terminal, you can check that by running ``` date ``` on all the nodes and comparing the results.

If the timezones are different, you can change them by running the command ``` sudo dpkg-reconfigure tzdata ```
 (again, on Ubuntu) and following the prompts.

#### Step 1
#### Step 2
#### Step 3

## Running the Simulation

On each of the nodes, run the generic_simulation() function from the [Simulation module](https://github.com/tudorelu/fahad_blockchain/blob/master/Simulation/Simulation.py).

Using the terminal, ```cd``` inside the main project folder (fahad_blockchain) and run the command ``` python3 ```

Once python initializes, run the following commands:

```py

from Simulation.Simulation import Simulation

Simulation.generic_simulation()

```
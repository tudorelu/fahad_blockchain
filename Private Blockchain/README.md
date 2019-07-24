# Private Blockchain Instructions

## Init Instructions

### On Initial Node

First, initialize private blockchain from genesis file:

```sh
geth --identity 898911 init Private\ Blockchain/genesis.json --datadir Private\ Blockchain/ChainData 

geth --identity 13373 init --datadir privatenet genesis.json
```

Then start the network and check out the enode id.

```sh
geth --datadir Private\ Blockchain/ChainData --networkid 898911 --rpc --rpcport 8543 --rpcaddr 127.0.0.1 --rpccorsdomain "*" --rpcapi "eth,net,web3,personal,miner" console

geth --datadir privatenet --networkid 13373 --port 31333 --rpc --rpcport 8538 --rpcaddr 127.0.0.1 --rpccorsdomain "*" --rpcapi "eth,net,web3,personal,miner" console --nodiscover
```

```py
admin.nodeInfo.enode 

# will give you something like
# enode://36e68383558a83cb524074530feac5884c04b84d2d49115e7a339a4a1e0e103db50eaec0bbcd2a0f3b82d065ce439428c1c365fc12d89e7bccf45ef7c1371e3f@203.214.112.190:62295?discport=0

```
Then copy the resulting enode.

### On Subsequent Nodes


#### Step 0

Please make sure that the remote nodes are on the same time zone as the initial node, and that the times match.

On an Ubuntu terminal, you can check that by running the following command on all the nodes and comparing.

```sh 
date 
```
If the timezones are different, you can change them by running the command (again, on Ubuntu):
```sh
sudo dpkg-reconfigure tzdata
```
And following their prompts.

#### Step 1

First, initialize private blockchain from genesis file:

```sh
geth --identity 769769 init Private\ Blockchain/genesis.json --datadir Private\ Blockchain/data 
```

#### Step 2

Then, start the network and add the initial node as a peer.

```sh
geth --datadir Private\ Blockchain/data --networkid 769769 --port 30303 --rpc --rpcport 8543 --rpcaddr 127.0.0.1 --rpccorsdomain "*" --rpcapi "eth,net,web3,personal,miner" console
```

#### Step 3

```py
admin.addPeer("enode://36e68383558a83cb524074530feac5884c04b84d2d49115e7a339a4a1e0e103db50eaec0bbcd2a0f3b82d065ce439428c1c365fc12d89e7bccf45ef7c1371e3f@203.214.112.190:62295?discport=0")
```

## Mining

To connect to private blockchain from second console window

```sh
geth attach http://127.0.0.1:8543
```

Then, to create a new account and to start mining in it:

```py
web3.personal.newAccount("")
miner.start()
```

To unlock account for 3600 seconds, which will allow you to run the simulation (assuming the passphrase for the account is ""):

```py
web3.personal.unlockAccount(web3.personal.listAccounts[0], "", 3600)
```

To stop the mining, type:

```py
mining.stop()
```

## Running the Simulation

On each of the nodes, run the generic_simulation() function from the [Simulation module](https://github.com/tudorelu/fahad_blockchain/blob/master/Simulation/Simulation.py).

Inside the main folder (fahad_blockchain), open python3 in a command line:

```sh
python3
```

And run:

```py

from Simulation.Simulation import Simulation

Simulation.generic_simulation()

```
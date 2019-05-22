
To initialize private blockchain from genesis file, type:

```sh
geth --identity 898911 init Private\ Blockchain/genesis.json --datadir Private\ Blockchain/ChainData
```

To connect to private blockchain:

```sh
geth --datadir Private\ Blockchain/ChainData --networkid 898911 --rpc --rpcport 8543 --rpcaddr 127.0.0.1 --rpccorsdomain "*" --rpcapi "eth,net,web3,personal,miner" console

admin.addPeer("enode://36e68383558a83cb524074530feac5884c04b84d2d49115e7a339a4a1e0e103db50eaec0bbcd2a0f3b82d065ce439428c1c365fc12d89e7bccf45ef7c1371e3f@203.214.112.190:62295?discport=0")

```

To connect to private blockchain from second console window

```sh
geth attach http://127.0.0.1:8543
```

Then, to create a new account and to start mining in it:

```py
web3.personal.newAccount()
miner.start()
```

To unlock account for 1000 seconds (assuming passphrase is ""):

```py
web3.personal.unlockAccount(web3.personal.listAccounts[0], "", 1000)
```



Find how to connect to private blockchain from another machine. Maybe it has something to do with 
adding an already running node as a bootnode:

admin.addPeer("enode://50c5f812da8c8eab832fa29258e683132b36ace28f9fe3be908e5ff33981f27dcaa13901089827f22a3d8693fd6e6cecdf629683fdde32695bd2ae1961a7dab5@203.214.112.190:30303?discport=0")

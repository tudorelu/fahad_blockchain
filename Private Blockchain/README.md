
To initialize private blockchain from genesis file, type:

```sh
	geth --identity 11111 init genesis.json --datadir Data
```

To connect to private blockchain:

```sh
geth --datadir Data --networkid 11111 --rpc --rpcport 8543 --rpcaddr 127.0.0.1 --rpccorsdomain "*" --rpcapi "eth,net,web3,personal,miner"
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

enode://6e1de03204cd6136c99a665b5c11eba57639b5389455d76299e9aab2fb6c7dc4bc6d139d42a5e6f5eb74bbd81421950bbb418692ce32daad018007709c364963@127.0.0.1:30303

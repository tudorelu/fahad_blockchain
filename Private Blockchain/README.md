
To initialize private blockchain from genesis file, type:

```sh
	geth --identity 11111 init genesis.json --datadir Private\ Blockchain/BlockchainData/Main
```

To connect to private blockchain:

```sh
geth --datadir Private\ Blockchain/BlockchainData/Main --networkid 11111 --rpc --rpcport 8543 --rpcaddr 127.0.0.1 --rpccorsdomain "*" --rpcapi "eth,net,web3,personal,miner" console < admin.addPeer("enode://9137389b92b6ff262c71c29cb9023293753b672d26cb5a7eae2e64c0b289734f0ac2f0aa65bb700a06447e6480ca17376a0f7f8eac13e470c6fd6efad3840b75@203.214.112.190:60006?discport=0")

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

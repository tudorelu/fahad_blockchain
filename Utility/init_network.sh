
geth --identity 898911 init Private\ Blockchain/genesis.json --datadir Private\ Blockchain/ChainData

geth --datadir Private\ Blockchain/ChainData --networkid 898911 --rpc --rpcport 8543 --rpcaddr 127.0.0.1 --rpccorsdomain "*" --rpcapi "admin,eth,net,web3,personal,miner" --nodiscover console


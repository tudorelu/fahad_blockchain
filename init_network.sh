
geth --identity 11111 init Private\ Blockchain/genesis.json --datadir Private\ Blockchain/BlockchainData/Main

geth --datadir Private\ Blockchain/BlockchainData/Main --networkid 11111 --rpc --rpcport 8543 --rpcaddr 127.0.0.1 --rpccorsdomain "*" --rpcapi "admin,eth,net,web3,personal,miner" --port 0 &


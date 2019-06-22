
echo admin.addPeer("enode://078dc48ba6929b76a08d6ced76a7df81ec6f1f72238c7c376ab3483bff96bf3ce95312ff973228afd1b80b90856d89ce823028d0fa9275ed6f5e10b26e7b3b85@203.214.112.190:30303?discport=0")

geth --datadir Private\ Blockchain/ChainData --networkid 898911 --rpc --rpcport 8543 --rpcaddr 127.0.0.1 --rpccorsdomain "*" --rpcapi "admin,eth,net,web3,personal,miner" --nodiscover console


There are 10 AWS Istances:

[Image]

###
We're connecting to each of them through ssh, running the command ` ssh -i off-chain-storage-nvirginia.pem ubuntu@<PUBLIC_DNS_ADDRESS> ` on 10 diferrent terminal windows, where everything coming after `ubuntu@` is one instance's public DNS address. To find all the addresses look inside instances.md.

**NOTE**: This must be called from within the root folder, where the off-chain-storage-nvirginia.pem file resides.

###
Then, we're installing the dependencies. Check Utility/instance_pre_install.sh 

###
Clone the repo on all instances.

` git clone https://github.com/tudorelu/fahad_blockchain `

Inside the Private Blockchain folder resides genesis.json, the file which generates the genesis block. It must be the same on each instance, so that when we're running the nodes we can connect them to each other.

Next, we'll initialize the blockchain (therfore creating the genesis block) on each of the instances, including on out personal computer by running from inside Private Blockchain\ 

` geth --identity 13373 init --datadir privatenet genesis.json `

Then, to run the nodes, we run on each instance (and on our computer):

` geth --datadir privatenet --networkid 13373 --port 31333 --rpc --rpcport 8538 --rpcaddr 127.0.0.1 --rpccorsdomain "*" --rpcapi "eth,net,web3,personal,miner" console `

After the node is running, on our computer only we type the command ` admin.nodeInfo.enode ` which will give you something like *enode://<ENODE_ID>*. 

Then, on each instance we type admin.addPeer("enode://<ENODE_ID>") and hit ENTER, which will make each node connect to the node on our computer. 

geth --identity 13373 init --datadir privatenet genesis.json 

cd Private\ Blockchain

geth --datadir privatenet --networkid 13373 console 

cd Private\ Blockchain

geth --datadir privatenet --networkid 13373 --port 31333 --rpc --rpcport 8538 --rpcaddr 127.0.0.1 --rpccorsdomain "*" --rpcapi "eth,net,web3,personal,miner" console 
admin.addPeer("enode://e7a2645d3db7a9ea421d0b99f72c3d8d5a64cc978cadc79f311498d2400b4f888b27593ab2abd9873e4b731a3fa1272c699852db76f032c367905e882f9fc663@18.212.25.187:31333")

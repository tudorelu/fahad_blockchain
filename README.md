# Project Overview
                    
   &nbsp;&nbsp; The purpose of this project is to create a secure, off-chain database that can be used in parralel with an on-chain smart contract and to provide the security of the blockchain to the off-chain database without the overhead of trying to put the entire database on the blockchain.

   &nbsp;&nbsp; The system comprises of 4 modules - a *smart contract* defining the identity of the entities interacting within the system, a *database* which holds the data of the entities, an *interface* which connects the smart contract to the database and enables the secure interaction between the two and a *simulation* script which tests the speed and security of the whole system.
 
                                                                     
## 1. [A SMART CONTRACT module](https://github.com/tudorelu/fahad_blockchain/blob/master/Interface/contract_source_code.py)

### Contents

  &nbsp;&nbsp; Written in _solidity_, for the ethereum network, which defines the *identity* and *access rights* side of this project. 

  &nbsp;&nbsp; This contract defines the entity base-structure and three separate entities - agent, organization and device. Entities interact with each other, by reading and writing data to and from one another. Entities have a tier-based leveling system, meanng that the higher their tier, the more access they have.

#### Entity

  &nbsp;&nbsp; An entity holds information about itself, like it's uniqueId (address), tier (level within an org), it's creatorId and it's dataHash (will talk more about it in the [database](https://github.com/tudorelu/fahad_blockchain#2-a-database) and [interface](https://github.com/tudorelu/fahad_blockchain#3-a-blockchain-data-interface) sections. It also contains info about other agents, like whi has access to it's data and what kind of access rights they have.

```js
    struct Entity {
        address payable         uniqueId;               // address used as an unique identifier
        int                     tier;                   // determines the level of importance and access rights
        bytes32                 dataHash;               // hash of data stored in DB for this Entity; used against data tampering
        address                 creatorId;              // address of creator of this entity
        
        // This mapping determines whether an Agent has access to this Entity's private data 
        mapping(address => bool)    
        agentsAccess;
        
        // This mapping determines  
        //    - what data can an Agent (address) access and 
        //    - what type of access does an Agent have to this Entity's data
        mapping(address => mapping(bytes32 => AccessType))     
        agentsAccessRights;

        
        // In the future, we will either have agentsAccess and agentsAccessRights turn into entitiesAccess and entitiesAccessRights, 
        // covering all entities within the two mappings or we will create two swparate mappings for each entity type.
        
    }
```

#### Agent (Individual)
  
  &nbsp;&nbsp; An agent can be simply understood as an individual. The agent's tier gives it it's status. Under any given scenario, different individuals will have different statuses.

  &nbsp;&nbsp; For *example*, for hospitals, we may have patients (Tier 0), visitors (Tier 1), nurses (Tier 2) and doctors (Tier 3). Thus, the tiers define a hierarchy. Higher tiered agents, such as doctors are able to access and validate information regarding lower tiered agents such as patients. For example, a doctor may admit a patient into a hospital. However, another patient won't be able to admit a patient, nor a visitor.
  
```js
    struct Agent {
        Entity          ent;
        address         orgId;                      // id of Organization this Agent belongs to
    }
```
#### Organization (Group)

  &nbsp;&nbsp; An organization is simply an entity under which a group of agents operate. A hospital (Tier 0) might be one; or a police station. Higher-tiered orgs are entities under which both agents and lower-tiered orgs operate - such as a ministry. 

  &nbsp;&nbsp; Continuing with the hospital *example*, the Ministry for Health (Tier 1 org) should have a minister (Tier 3 agent) and a lot of public servants (Tiers 0-2) operating under it, plus a bunch of hospitals and insurance agencies (Tier 0 orgs) that are recognized by this Ministry. However, a minister, which is a top-tiered agent in a ministry doesn't have the access rights of doctors, nor even of nurses or patients for an individual hospital, unless expressly given.

  &nbsp;&nbsp; Higher tiered entities can validate/approve lower tiered ones. For example, Ministeries can determine whether an org can be considered a hospital or not and doctors and nurses can determine wether somebody is a patient to a hospital.

```js
    struct Organization {
        Entity          ent;
        address         adminId;                    // address of Organization's admin
        int             maxAgentTier;               // max tier that a member of this Org can have
        
        mapping(address => bool)    agentMembers;   // list of agent members of this Organization
        mapping(address => bool)    orgMembers;     // list of org members of this Organization
    }
```
#### Device (IoT, Mobile Phone, Smart Watch, etc)
 
  &nbsp; &nbsp; The purpose of a device is to collect info about an agent (IE collecting vitals of patients in a hospital setting), an org (air quality in a city or factory) or something related to the system.
  
```js
    struct Device {
        Entity          ent;
        address         adminId;                    // the administrator/owner of this device
        address         userId;                     // the current user of this device
    }
```

## 2. [A DATABASE module](https://github.com/tudorelu/fahad_blockchain/tree/master/Database)

  &nbsp;&nbsp; A _json_ (nosql) database which handles the *data* part of this project.

  &nbsp;&nbsp; This contains details about each agent, org and device. Each entity has access to it's own data. If one entity wants to access another ones' data, the blockchain is checked through the smart contract to see whether the accessing entity is allowed to.

  &nbsp;&nbsp; The data repository is a database that can be hosted on a server, or on a local machine, and copies of it are shared on all the nodes. It holds each entity's information, it's history, it's relation to other entities and it's access rights. The database is connected to the smart contract through the third module, the interface. 

  &nbsp;&nbsp; Data integrity of each individual entity is maintained by saving the hash of their database entries within the blockchain (dataHash field inside the Entity struct). The blockchain allows either the contract owner (the administrator who initialized this system) or the entity itself to save that dataHash, by calling a function on the smart contract which can only be called using their accounts.


### 3. [A blockchain-data INTERFACE module](https://github.com/tudorelu/fahad_blockchain/tree/master/Interface)

  &nbsp;&nbsp; Written in _python_, using web3.py that handles the *logic* of this system.

  &nbsp;&nbsp; The interactions between the smart contract and the data happens through this module, such as instantiation of new entities, changing tier levels, changing access rights or changing the data in any way. When somebody tries to change the database through the interface, first the blockchain will be consulted to check whether that entity is allowed to. Once they do, the new database hash is saved. If somebody changes the database outside of the interface, we will know that has happened and where the data was changed and the new data won't be valid.

### 4. [A SIMULATION module](https://github.com/tudorelu/fahad_blockchain/tree/master/Simulation)

  &nbsp;&nbsp; Written in _python_ and handles the *SIMULATION* of a potential real-world scenario which uses our system.

  &nbsp;&nbsp; This will determine the number of entities that will exist in the simulation, how often they will interact with each other and test the speed at which the system runs. Things such as the read and write time of information from the data repo will be tested, or the changing of access rights of entities, which will require the use of blockchain.

### 5. [A PRIVATE BLOCKCHAIN module](https://github.com/tudorelu/fahad_blockchain/tree/master/Private%20Blockchain)

  &nbsp;&nbsp; In order to properly simulate the speed of the system, we needed to create a private blockchain and add a number of nodes to it. 

#### First Node

  &nbsp;&nbsp; First, we initialized a private blockchain on one of our personal computers and ran the geth node software on our computer, making it the first node on our blockchain. Then, we copied this node's enode id.

#### Subsequent Nodes

  &nbsp;&nbsp; Next we instantiated multiple AWS servers to create the other nodes. Once a server was created, we ran a few commands to install the prerequisites, initialize the blockchain locally (using the same parameters as the first node), run the geth node software and then to connect to the initial node that was on the chain using the enode id that we copied initially.

# Installation Prerequisites

## SYSTEM
[python >= 3.6](http://lmgtfy.com/?q=install+python3)

[ethereum & geth](https://github.com/ethereum/go-ethereum/wiki/Building-Ethereum)

[solidity compiler](https://solidity.readthedocs.io/en/v0.5.3/installing-solidity.html#binary-packages)


## PYTHON3 

First install the pip3 ([ubuntu](https://linuxize.com/post/how-to-install-pip-on-ubuntu-18.04/), [mac](https://evansdianga.com/install-pip-osx/) or [windows](http://lmgtfy.com/?q=install+pip3+on+windows)) package manager, in order to be able to install the other useful packages.

On Ubuntu 18

```sh
sudo apt update
sudo apt install python3-pip
```

```sh
# Web3 (Interface Connecting to ETH network )
pip3 install web3

# Solidity Compiler
pip3 install py-solc-x

#Ethereum Key Utilities
pip3 install eth_keys
pip3 install eth_utils

#Ellyptic Curve Cryptography for Wallet Generation
pip3 install eciespy

```

# Progress

  &nbsp;&nbsp; Because of time constraints we couldn't implement the complete functionality of all the above modules, however we implemented the minimal requirements allowing us to run the simulation.

  &nbsp;&nbsp; For the purpose of the first paper -> *to simulate the speed with which multiple entities interact securely, with each-other through this on and off-chain system*, the agents are the entities who have most of the functionality developed, so in the simulation the intercation that is being run is between multiple agents. This runs at exactly the same speed as running it benween any other two entities, because in the smart contract the entities are defined using almost the same variables, and inside the interface the function for saving inside the database within any Entity's data takes the same amount of time.

## PROJECT OVERVIEW
                    
   This project contains 3 or 4 main modules:
 
                                                                     
### 1. A SMART CONTRACT 

  &nbsp;&nbsp; Written in _solidity_, for the ethereum network, which defines the *IDENTITY* side of this project. 

  &nbsp;&nbsp; This contract defines two entities - agent and party. There are multiple tiers of each of these entities; each entity can have different importance levels. Entities interact with each other, can validate one another and sometimes are inter-depend. 
  
  #### Agent (individual)
  
  &nbsp;&nbsp; An agent can be simply understood as an individual. The agent's tier 
  gives it it's status. Under any given scenario, different individuals 
  will have different statuses.

  &nbsp;&nbsp; For *EXAMPLE*, for hospitals, we may have 
  patients and visitors (Tier 0), nurses (Tier 1) and doctors (Tier 2) 
  as agents. Thus, the tiers define a hierarchy. Higher tiered agents,
  such as doctors are able to access and validate information regarding
  lower tiered agents such as patients. For example, a doctor may admit
  a patient into a hospital. However, another patient won't be able to.
  
  #### Party (organization)

  &nbsp;&nbsp; A party can be understood as an organization. It is simply an entity under which a group of agents operate. A hospital (Tier 0) might be a party; or a police station might be one. Higher-tiered parties are entities under which both agents and lower-tiered parties operate - such as a ministry. 

  &nbsp;&nbsp; Continuing the same, hospital
  *EXAMPLE*, the Ministry for Health (Tier 1 party) should have a minister 
  (Tier 3 agent) and a lot of public servants (Tiers 0-2) operating 
  under it, plus a bunch of hospitals (Tier 0 party) that are recognized 
  by this Ministry. However, a minister, which is a top-tiered agent in 
  a ministtry doesn't have the access rights of doctors, nor even of 
  nurses or patients for an individual hospital, unless expressly given 
  (IE unless they're also a doctor in that hospital).

  &nbsp;&nbsp; More generally, for agents, tires are in relation to the party under 
  which they operate.

  &nbsp;&nbsp; Higher tiered entities can validate/approve lower tiered ones. For 
  example, Ministeries can determine whether a party can be considered 
  a hospital or not and doctors and nurses can determine wether somebody 
  is a patient to a hospital.

  #### Device (iot or mobile)
 
 &nbsp; &nbsp; The purpose of a device is to collect data about an agent (IE collecting vitals of patients in a hospital setting), a party (air quality in a city or factory) or something related to the system.
 
 
### 2. A DATABASE 

  &nbsp;&nbsp; Format tbd, probably _sql or json_, which handles the *DATA* part of this project.

  &nbsp;&nbsp; This is a centralized data repository, which contains details about
  each agent and party. Each entity has access to it's own data. Higher 
  tiered entities may be able to access some lower tiered entity's data.

  &nbsp;&nbsp; All entities are uniquely identifiable based on their public keys and 
  may make changes to the data repository based on their access rights.

  &nbsp;&nbsp; The data repository is a database that will be hosted on a server. It 
  holds each entity's information, it's history, it's relation to other 
  entities and it's access rights. The database will be connected to the
  smart contract through the third module.

### 3. A blockchain-data INTERFACE 

  &nbsp;&nbsp; Probably written in _python_, using web3.py that handles the *LOGIC* of this system. (ADMIN SCRIPT)

  &nbsp;&nbsp; The interactions between the smart contract and the data will happen
  through this module, such as instantiation of new entities, changing
  tier levels, changing access rights or changing the data in any way.

  &nbsp;&nbsp; This program will be able to accept parameters such as what types of 
  entities there should exist and how they will interact with each other.
  Also, it will determine the access rights and the actions that can be 
  taken by the different tier levels. 

                                                                     
  ### 4. A SIMULATOR 

  &nbsp;&nbsp; Probably also written in _python_ and handles the *SIMULATION* of a potential real-world scenario which uses our system.

  &nbsp;&nbsp; This will determine the number of entities that will exist in the 
  simulation, how often they will interact with each other and test the
  speed at which the system runs, given different levels of stress.

  &nbsp;&nbsp; Things such as the read and write time of information from the data 
  repo will be tested, or the changing of access rights of entities, 
  which will require the use of blockchain.

  &nbsp;&nbsp; Modules 3 and 4 might be combined into a single program.


## TECHNICAL CONSIDERATIONS & PROJECT STRUCTURE
                           
### Smart Contract 
  
  + written in Solidity
  + defines agents and parties
  + handles identity management
  + holds basic access rights information (through the tier system)
  
#### This module will contain the following:

##### The Entity 'class', which contains:
     
   _Properties:_
   
      address entityId     - address used to uniquely identify entity
      int tier             - used to determine the tier number

##### The Agent (Member, or Individual) class, which extends Entity and contains:
 
   _Properties:_
   
      address partyId       - address of party to which this agent pertains (can only pertain to one party!?)


##### The Party (Organisation or Institution) class, which also extends Entity and contains:

   _Properties:_
   
      address adminId       - address of admin of party (which can add or remove agents and change their rights within party)
      [address] members     - a list of addresses of agents pertaining to this party
      [address] subparties  - a list of addresses of parties pertaining to this one (that are of lower tier?)
      int maxTier           - integer determining the maximum tier level an agent can have within this party

   _Methods:_
   
      removeEntity(address entityId):
          removes entity from party
          
      changeTierLevel(address entityId, int newTier): 
          changes the tier level of a given entity, if called by admin
      
      initiateChangeAdmin(address newAdminId): 
          initiates the change to a new admin (function called by current Admin)
      
      finalizeChangeAdmin(): 
          should be called after initializeChangeAdmin(newAdminId) was called, 
          by owner of the private key of address newAdminId (potential new admin)


##### The Device class, which extends Entity and contains:
 
   _Properties:_
   
      address adminId       - address of agent / party who has admin access to this data source
      
      
##### The system admin / owner, which also extends Entity and has hard-coded full access to all methods
    
   _Methods:_
    
      changeTierLevel(address partyId, address entity, int newTier): 
          changes the tier level of a given entity

### Database
  
  + SQL or json 
  + hosted locally or on the web
  + holds information about entities
  + holds more detailed access-rights information

#### This module will contain the following:
  
  + Check the database_structure.json file
 
### Interface
  
  + written in Python 
  + defines systems' parameters (inputs)
  + uses web3.py for interfacing with the ethereum network
  + compiles and launches the smart contract based on params  
  + provides the connection between the smart contract and the database 

#### This module will contain the following:
  
  + TBD by week 3
 
### Simulator
  
  + written in Python
  + used to speed test the system

#### This module will contain the following:
  
  + TBD by week 3

   Since the Identity management will be handled through a smart contract on top of the blockchain, and the blockchain will hold information about the tier levels of the individual entities, the only kind of action that will be dependent upon the TX speed of the blockchain is the changing of tier levels for entities. 


## MILESTONES

### Week 1 (1st - 7th April)

#### Smart Contract Module

  [Defines entities & basic functionality]()
    
  + define entity, agent & party
  + methods: assign agent to party, assign admin to party

#### Database Module

  [Define general structure of database]()

#### Overall

  Plan what methods will be handled by the smart contract module and which ones by the interface module.
  
  Anything pertaining to reading access rights, storing tier levels and basic organisational structure (IE basic authentication) will be handled by the blockchain, anything more complicated than that should be handled by the interface.

### Week 2 (8th - 14th April)

#### Smart Contract Module

  Define advanced functionality

#### Database Module

  Create DB based on general structure
  Populate with mock data, for testing (10-20 items)

#### Interface Module (basic functionality)
    
  Basic bockchain interaction
    
  + read data
  + call functions

  Basic DB interaction
    
  + read & write

### Week 3 (15th - 21st April)

#### Smart Contract Modules

  Launch contract on testnet
  
#### Interface Module (advanced functionality)

  Blockchain functionality
    
  + programatically launch smart contract on testnet
    
  Blockchain to DB interaction  
    
  + write functions to connect the two modules
  + be able to write to DB only if blockchain permits and vice-versa
  + be able to write to DB by using he encrypted private key of uniqueId

#### Simulation Module

  Defne simulation scenatio
  
### Week 4 (22nd - 28th April)

#### Simulation Module
  
  Develop and run simulation scenario

### Week 5 (29th April - 6th May)

#### Overall

  Putting it all together

## MISCELLANEOUS

### USE CASES
 
Reading data from the data repository works as such:

An entity makes a request to read data

    If the data is publicly available, it is read from the DB and shown to the entity. 
    
    Otherwise:
        - If the request contained the sender's private key and if the sender has access to the data, then it will be shown
        - Otherwise it won't be shown, stating 'access denied'

 ### Reserach Links

   [Blockchain IOT Market - Global forecast for 2024](https://www.marketsandmarkets.com/Market-Reports/blockchain-iot-market-168941858.html)
   
   [IOTeX Research (blockchain IOT project)](https://iotex.io/academics)
   
   [Holochain - worth looking into for v3 of this system](https://holochain.org/)

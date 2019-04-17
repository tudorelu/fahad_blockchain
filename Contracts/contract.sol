pragma solidity >=0.4.22 <0.6.0;

    /**
     * This contract defines the interactions between three entities - agent, 
     * party and device. There are different tiers for each of these entities, 
     * defining different importance levels. All these entities interact with 
     * each other, can validate one another and sometimes are inter-depend.
     * 
     * There is a centralized data repository, which contains details about
     * each agent and party. Each entity has access to it's own data. Higher 
     * tiered entities may be able to access some lower tiered entity's data.
     * 
     * This smart contract handles the identity of the system.
     *
     * All entities are uniquely identifiable based on their public keys and 
     * may make changes to the main data repository based on their access 
     * rights and private keys.
     * 
     * Higher tiered entities can validate/approve lower tiered ones. For
     * example, Ministeries can determine whether a party can be considered 
     * a hospital or not and doctors and nurses can determine wether somebody 
     * is a patient to a hospital.
     * 
     **/

/**
 * Defines the main contract which allows the interaction between devices, agents and parties
 * */

//import './Organization.sol';

contract System {
    
    address payable admin;
    
    mapping(address => bool) orgs;
    mapping(address => bool) agents;
    
    struct Entity {
        address payable uniqueId;                   // used as a unique id
        int             tier;                       // determines the access rights
    }
    
    struct Agent {
        Entity          ent;
        address         orgId;                      // id of organization this Agent belongs
    }
    
    struct Organization {
        Entity          ent;
        address         adminId;                    // address of Organization admin
        int             maxAgentTier;               // max tier of Organization members
    }
    
    struct Device {
        Entity          ent;
    }
    /* The list of agents that belong to each organization.
        First address is the uniqueId of an organization;
        Second address is the uniqueId of an Agent;
    */
    mapping(address => mapping(address => Agent)) organizationAgents;
    mapping(address => mapping(address => Organization)) organizationOrgs;
    
    constructor () public {
        admin = msg.sender;
    }
    
    /*  Validates address as being of an Agent's by adding it to list of valid Agents. */
    function createNewAgent (address payable _agentId) public {
        agents[_agentId] = true;
    }
    
    /* Check whether address belonngs to a valid Agent */
    function isAgent (address payable _agentId) public view returns (bool) {
        return agents[_agentId];
    }
    
    /* Revokes the address' validity as being of an agent's by removing it from list of Agents. */
    function removeAgent (address payable _agentId) public {
        agents[_agentId] = false;
    }        
    
    /*  Validates address as being of an Organization by adding it to list of valid Orgs. */
    function createNewOrganization (address payable _orgId) public {
        orgs[_orgId] = true;
    }
    
    /* Check whether address belonngs to a valid Organization */
    function isOrg (address payable _orgId) public view returns (bool) {
        return orgs[_orgId];
    }        

    /* Revokes the address' validity as being of an organization's by removing it from list of Orgs. */
    function removeOrganization (address payable _orgId) public {
        orgs[_orgId] = false;
    }
    
    function assignAgentToOrganization (address payable _agentId, address payable _orgId) public {
        require(agents[_agentId]);
        
        Agent memory agent;
        agent.ent.uniqueId = _agentId;
        agent.orgId = _orgId;

        organizationAgents[_orgId][_agentId] = agent;
        
    }
    
}

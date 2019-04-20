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
    
    address payable admin;                          // system admin
    
    mapping(address => bool) validOrgs;             // all valid organizations
    mapping(address => bool) validAgents;           // all valid agents
    
    struct Entity {
        address payable uniqueId;                   // used as a unique id
        int             tier;                       // determines the access rights
    }
    
    struct Agent {
        Entity          ent;
        address         orgId;                      // id of Organization this Agent belongs to
    }
    
    struct Organization {
        Entity          ent;
        address         adminId;                    // address of Organization admin
        int             maxAgentTier;               // max tier of Organization members
    }
    
    struct Device {
        Entity          ent;
    }

    mapping(address => Agent)           agentsList;             // list of all existing Agents
    mapping(address => Organization)    orgsList;               // list of all existing Orgs
    mapping(address => Device)          devicesList;            // list of all existing Devices

    /* The list of Agents that belong to each Organization;
        First address is the uniqueId of an Organization;
        Second address is the uniqueId of an Agent.
    */
    mapping(address => mapping(address => Agent)) organizationAgents;

    /* The list of Organizations that are under each Org;
        First address is uniqueID of parent Org;
        Second address is uniqueId of child Org. 
    */
    mapping(address => mapping(address => Organization)) organizationOrgs;
    
    modifier onlyOwner() {
        require(msg.sender == admin, "Only the system admin can make this call.");
        _;
    }

    modifier onlyAddress(address _address) {
        require(msg.sender == _address, "Unauthorized sender.");
        _;
    }

    modifier mustBeAgent(address payable _address) {
        require(validAgents[_address], "Address not a valid agent.");
        _;
    }

    modifier mustBeOrg(address payable _address) { 
        require (isOrganization(_address), "Address not a valid organization."); 
        _; 
    }

    constructor () public {
        admin = msg.sender;
    }
    
    /*  Validates address as being of an Agent's by adding it to list of valid Agents. */
    function createNewAgent (address payable _agentId) public onlyOwner() {
        validAgents[_agentId] = true;
        
        Agent memory agent;
        agent.ent.uniqueId = _agentId;
        agent.ent.tier = 0;
        
        agentsList[_agentId] = agent;
        delete agent;
    }
    
    /* Check whether address belonngs to a valid Agent */
    function isAgent (address payable _agentId) public view returns (bool) {
        return validAgents[_agentId];
    }
    
    /* Revokes the address' validity as being of an agent's by removing it from list of Agents. */
    function removeAgent (address payable _agentId) public onlyOwner() {
        validAgents[_agentId] = false;
        delete agentsList[_agentId];
    }        
    
    /*  Validates address as being of an Organization by adding it to list of valid Orgs. */
    function createNewOrganization (address payable _orgId, address payable _adminId) public onlyOwner() mustBeAgent(_adminId) {
        require(isAgent(_adminId));
        validOrgs[_orgId] = true;
        
        Organization memory org;
        org.ent.uniqueId = _orgId;
        org.ent.tier = 0;
        org.adminId = msg.sender;
        org.maxAgentTier = 8;

        orgsList[_orgId] = org;
        delete org;
    }
    
    /* Check whether address belonngs to a valid Organization */
    function isOrganization (address payable _orgId) public view returns (bool) {
        return validOrgs[_orgId];
    }        

    /* Revokes the address' validity as being of an organization's by removing it from list of Orgs. */
    function removeOrganization (address payable _orgId) public onlyOwner() mustBeOrg(_orgId){
        validOrgs[_orgId] = false;
        delete orgsList[_orgId];
    }
    
    function assignAgentToOrganization (address payable _agentId, address payable _orgId) public 
    onlyAddress(orgsList[_orgId].adminId) 
    mustBeAgent(_agentId)
    mustBeOrg(_orgId) {
        
        Agent memory agent;
        agent.ent.uniqueId = _agentId;
        agent.orgId = _orgId;

        organizationAgents[_orgId][_agentId] = agent;
        delete agent;
        
    }

    function changeAdminOfOrganization (address payable _adminId, address payable _orgId) public 
    onlyAddress(orgsList[_orgId].adminId) 
    mustBeAgent(_adminId)
    mustBeOrg(_orgId) {
        require(validAgents[_adminId] && validOrgs[_orgId]);

        Organization memory org = orgsList[_orgId];
        org.adminId = _adminId;
        orgsList[_orgId] = org;
        delete org;
    }
    
}

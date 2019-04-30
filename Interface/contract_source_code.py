source = '''
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
        address payable uniqueId;                   // address used as an unique identifier
        int             tier;                       // determines the level of importance and access rights
        string          dataHash;                   // hash of data stored in DB for this Entity; used against data tampering
    }
    
    struct Agent {
        Entity          ent;
        address         orgId;                      // id of Organization this Agent belongs to
    }
    
    struct Organization {
        Entity          ent;
        address         adminId;                    // address of Organization's admin
        int             maxAgentTier;               // max tier that a member of this Org can have
    }
    
    struct Device {
        Entity          ent;
        address         adminId;                    // the administrator/owner of this device
        address         userId;                     // the current user of this device
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

    modifier mustBeOrganization(address payable _address) { 
        require (isOrganization(_address), "Address not a valid organization."); 
        _; 
    }
    
    modifier mustNotBeOrganization(address payable _address) {
        require(!isOrganization(_address), "This address belongs to an organization. ");
        _;
    }
    
    constructor () public {
        admin = msg.sender;
    }
    
    /* ~~~~~~~~~~~~~~~~~~~~~~~~~~~~ AGENT FUNCTIONS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~ */ 
    
    /*  Validates address as being of an Agent's by adding it to list of valid Agents. */
    function createNewAgent (address payable _agentId, string memory _dataHash) public onlyOwner() {
        validAgents[_agentId] = true;
        
        Agent memory agent;
        agent.ent.uniqueId = _agentId;
        agent.ent.tier = 0;
        agent.ent.dataHash = _dataHash;
        
        agentsList[_agentId] = agent;
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
    
    /* Changes the tier of an Agent */
    function setAgentTier(address payable _agentId, int _tier) public onlyOwner() mustBeAgent(_agentId){
        Agent memory agent = agentsList[_agentId];
        agent.ent.tier = _tier;
        agentsList[_agentId] = agent;
    }
    
    /* Changes the dataHash of an Agent */
    function setAgentDataHash(address payable _agentId, string memory _dataHash) public onlyOwner() mustBeAgent(_agentId){
        Agent memory agent = agentsList[_agentId];
        agent.ent.dataHash = _dataHash;
        agentsList[_agentId] = agent;
    }    
    
    /* Shows details of Agent as saved on blockchain */
    function viewAgentDetails (address payable _agentId) public view returns (address, int, string memory, address) {
        return (agentsList[_agentId].ent.uniqueId, agentsList[_agentId].ent.tier,  agentsList[_agentId].ent.dataHash, agentsList[_agentId].orgId);
    }
    
    /* ~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ORGANIZATION FUNCTIONS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~ */
    
    /*  Validates address as being of an Organization by adding it to list of valid Orgs. */
    function createNewOrganization (address payable _orgId, address payable _adminId, string memory _dataHash) public 
    onlyOwner() 
    mustBeAgent(_adminId) 
    mustNotBeOrganization(_orgId){
        require(!isOrganization(_adminId), "Admin address belongs to an Organization. An Admin must be an Agent and can't be an Organization.");
        validOrgs[_orgId] = true;
        
        Organization memory org;
        org.ent.uniqueId = _orgId;
        org.ent.tier = 0;
        org.ent.dataHash = _dataHash;
        org.adminId = msg.sender;
        org.maxAgentTier = 8;

        orgsList[_orgId] = org;
    }
    
    /* Check whether address belonngs to a valid Organization */
    function isOrganization (address payable _orgId) public view returns (bool) {
        return validOrgs[_orgId];
    }        

    /* Revokes the address' validity as being of an organization's by removing it from list of Orgs. */
    function removeOrganization (address payable _orgId) public onlyOwner() mustBeOrganization(_orgId){
        validOrgs[_orgId] = false;
        delete orgsList[_orgId];
    }
    
    /* Changes the dataHash of an Organization */
    function setOrganizationDataHash(address payable _orgId, string memory _dataHash) public onlyOwner() mustBeOrganization(_orgId){
        Organization memory org = orgsList[_orgId];
        org.ent.dataHash = _dataHash;
        orgsList[_orgId] = org;
    }
 
    /* Changes the tier of an Organization */
    function setOrganizationTier(address payable _orgId, int _tier) public onlyOwner() mustBeOrganization(_orgId){
        Organization memory org = orgsList[_orgId];
        org.ent.tier = _tier;
        orgsList[_orgId] = org;
    }
    
    /* Shows details of Organization as saved on blockchain */
    function viewOrgDetails (address payable _orgId) public view returns (address, int, string memory, address) {
        return (orgsList[_orgId].ent.uniqueId, orgsList[_orgId].ent.tier,  orgsList[_orgId].ent.dataHash, orgsList[_orgId].adminId);
    }
    
    /* Makes Agent be part of organization */
    function assignAgentToOrganization (address payable _agentId, address payable _orgId) public 
    onlyAddress(orgsList[_orgId].adminId) 
    mustBeAgent(_agentId)
    mustBeOrganization(_orgId) {
        
        Agent memory agent;
        agent.ent.uniqueId = _agentId;
        agent.orgId = _orgId;

        organizationAgents[_orgId][_agentId] = agent;

    }
    
    /* Changes admin of Organization */
    function changeAdminOfOrganization (address payable _adminId, address payable _orgId) public 
    onlyAddress(orgsList[_orgId].adminId) 
    mustBeAgent(_adminId)
    mustBeOrganization(_orgId) {
        require(validAgents[_adminId] && validOrgs[_orgId]);

        Organization memory org = orgsList[_orgId];
        org.adminId = _adminId;
        orgsList[_orgId] = org;
    }
    
    /* ~~~~~~~~~~~~~~~~~~~~~~~~~~~~ DEVICE FUNCTIONS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~ */
    
}
'''
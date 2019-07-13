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
    
    address payable             admin;                  // system admin
    
    mapping(address => bool)    validOrgs;             // all valid organizations
    mapping(address => bool)    validAgents;           // all valid agents
    mapping(address => bool)    validDevs;             // all valid devices
    
    mapping(address => Agent)           agentsList;     // list of all existing Agents
    mapping(address => Organization)    orgsList;       // list of all existing Orgs
    mapping(address => Device)          devsList;       // list of all existing Devices

    /* ~~~~~~~~~~~~~~~~~~~~~~~~~~~ STRUCTS ~~~~~~~~~~~~~~~~~~~~~~~~~~~ */ 
    //{
    struct Entity {
        address payable         uniqueId;               // address used as an unique identifier
        int                     tier;                   // determines the level of importance and access rights
        bytes32                 dataHash;               // hash of data stored in DB for this Entity; used against data tampering
        address                 creatorId;              // address of creator of this entity
        
        /* This mapping determines whether an Agent has access to this Entity's private data */
        mapping(address => bool)    
        agentsAccess;
        
        /* This mapping determines  
            - what data can an Agent (address) access and 
            - what type of access does an Agent have to this Entity's data */
        mapping(address => mapping(bytes32 => AccessType))     
        agentsAccessRights;
    }
    
    struct Agent {
        Entity          ent;
        address         orgId;                      // id of Organization this Agent belongs to
    }
    
    struct Organization {
        Entity          ent;
        address         adminId;                    // address of Organization's admin
        int             maxAgentTier;               // max tier that a member of this Org can have
        
        mapping(address => bool)    agentMembers;   // list of agent members of this Organization
        mapping(address => bool)    orgMembers;     // list of org members of this Organization
    }

    struct Device {
        Entity          ent;
        address         adminId;                    // the administrator/owner of this device
        address         userId;                     // the current user of this device
    }

    enum AccessType {
        NONE, READ, WRITE, ADMIN
    }
    
    //}
    /* ~~~~~~~~~~~~~~~~~~~~~~~~~~ MODIFIERS ~~~~~~~~~~~~~~~~~~~~~~~~~~ */ 
    //{
        modifier onlyAdmin() {
            require(msg.sender == admin, "Only the system admin can make this call.");
            _;
        }
        
        modifier onlyAdminAnd(address _address) {
            require(msg.sender == admin || msg.sender == _address, "Only the system admin and a specific address can make this call.");
            _;
        }
    
        modifier onlyAddress(address _address) {
            require(msg.sender == _address, "Unauthorized sender.");
            _;
        }
    
        modifier mustBeAgent(address payable _address) {
            require(validAgents[_address], "Address does not belong to a valid agent.");
            _;
        }
        
        modifier mustNotBeAgent(address payable _address) {
            require(!validAgents[_address], "Address belongs to an agent, but it should not.");
            _;
        }
    
        modifier mustBeOrganization(address payable _address) { 
            require (isOrganization(_address), "Address not a valid organization."); 
            _; 
        }
        
        modifier mustNotBeOrganization(address payable _address) {
            require(!isOrganization(_address), "This address belongs to an organization, but it should not.");
            _;
        }
        
        modifier mustBeDevice(address payable _address) { 
            require (isDevice(_address), "Address not a valid device."); 
            _; 
        }
        
        modifier mustNotBeDevice(address payable _address) {
            require(!isDevice(_address), "This address belongs to a device and it shouldn't.");
            _;
        }
            
    //}
    
    constructor () public {
        admin = msg.sender;
    }
    
    /* ~~~~~~~~~~~~~~~~~~~~~~~~~~~~ AGENT ~~~~~~~~~~~~~~~~~~~~~~~~~~~~ */ 
    //{
    /*  Validates address as being of an Agent's by adding it to list of valid Agents. */
    function createNewAgent (address payable _agentId, bytes32 _dataHash) public 
    mustNotBeAgent(_agentId)
    mustNotBeDevice(_agentId)
    mustNotBeOrganization(_agentId)
    //onlyAdmin()
    {
        Agent memory agent;
        agent.ent.tier = 0;
        agent.ent.uniqueId = _agentId;
        agent.ent.dataHash = _dataHash;
        agent.ent.creatorId = msg.sender;
        
        validAgents[_agentId] = true;
        agentsList[_agentId] = agent;
    }
    
    /* Check whether address belonngs to a valid Agent */
    function isAgent (address payable _agentId) public view 
    returns (bool) {
        return validAgents[_agentId];
    }
    
    /* Revokes the address' validity as being of an agent's by removing it from list of Agents. */
    function removeAgent (address payable _agentId) public 
    onlyAdminAnd(_agentId) 
    {
        validAgents[_agentId] = false;
        delete agentsList[_agentId];
    }        
    
    /* Changes the tier of an Agent */
    function setAgentTier(address payable _agentId, int _tier) public 
    onlyAdminAnd(_agentId) 
    mustBeAgent(_agentId){
        Agent memory agent = agentsList[_agentId];
        agent.ent.tier = _tier;
        agentsList[_agentId] = agent;
    }
    
    /* Changes the dataHash of an Agent */
    function setAgentDataHash(address payable _agentId, bytes32 _dataHash) public 
    mustBeAgent(_agentId)
    {
        Agent memory agent = agentsList[_agentId];
        require(msg.sender == agent.ent.creatorId || msg.sender == _agentId || msg.sender == admin, "This function can only be called by the agent, it's creator or the system admin. ");
        agent.ent.dataHash = _dataHash;
        agentsList[_agentId] = agent;
    }    
    
    /* Shows details of Agent as saved on blockchain */
    function viewAgentDetails (address payable _agentId) public view 
    returns (address, int, bytes32, address) {
        return (agentsList[_agentId].ent.uniqueId, agentsList[_agentId].ent.tier,  agentsList[_agentId].ent.dataHash, agentsList[_agentId].orgId);
    }
    
    /* Gets an Agent's access rights to another Agent's data */
    function getAgentAccessRightsToData(address payable _ownerId, address payable _accessorId, bytes32 accessPath) public view
    onlyAdminAnd(_ownerId)
    mustBeAgent(_ownerId)
    mustBeAgent(_accessorId)
    returns(AccessType){
        return agentsList[_ownerId].ent.agentsAccessRights[_accessorId][accessPath];
    }
    
    /* Gives an Agent access another Agent's data */
    function giveAgentAccessToData(address payable _ownerId, address payable _accessorId, AccessType accessType, bytes32 accessPath) public 
    onlyAdminAnd(_ownerId)
    mustBeAgent(_ownerId)
    mustBeAgent(_accessorId){
        Agent storage dataOwner = agentsList[_ownerId];
        dataOwner.ent.agentsAccess[_accessorId] = true;
        dataOwner.ent.agentsAccessRights[_accessorId][accessPath] = accessType;
        agentsList[_ownerId] = dataOwner;
    }
    
    /* Removes an Agent's access right to another Agent's data */
    function removeAgentAccessToData(address payable _ownerId, address payable _accessorId, bytes32 accessPath) public 
    onlyAdminAnd(_ownerId)
    mustBeAgent(_ownerId)
    mustBeAgent(_accessorId){
        delete agentsList[_ownerId].ent.agentsAccessRights[_accessorId][accessPath];
    }
    //}
    
    /* ~~~~~~~~~~~~~~~~~~~~~~~~~ ORGANIZATION ~~~~~~~~~~~~~~~~~~~~~~~~~ */
    //{
    /*  Validates address as being of an Organization by adding it to list of valid Orgs. */
    function createNewOrganization (address payable _orgId, address payable _adminId, bytes32 _dataHash) public 
    mustBeAgent(_adminId) 
    mustNotBeAgent(_orgId)
    mustNotBeDevice(_orgId)
    mustNotBeOrganization(_orgId){
        require(!isOrganization(_adminId), "Admin address belongs to an Organization. An Admin must be an Agent and can't be an Organization.");
        validOrgs[_orgId] = true;
        
        Organization memory org;
        org.ent.uniqueId = _orgId;
        org.ent.tier = 0;
        org.ent.dataHash = _dataHash;
        org.ent.creatorId = msg.sender;
        org.adminId = msg.sender;
        org.maxAgentTier = 8;

        orgsList[_orgId] = org;
    }
    
    /* Check whether address belonngs to a valid Organization */
    function isOrganization (address payable _orgId) public view returns (bool) {
        return validOrgs[_orgId];
    }        

    /* Revokes the address' validity as being of an organization's by removing it from list of Orgs. */
    function removeOrganization (address payable _orgId) public 
    onlyAdminAnd(_orgId) 
    mustBeOrganization(_orgId){
        validOrgs[_orgId] = false;
        delete orgsList[_orgId];
    }
    
    /* Changes the dataHash of an Organization */
    function setOrganizationDataHash(address payable _orgId, bytes32 _dataHash) public 
    //onlyAdminAnd(_orgId) 
    mustBeOrganization(_orgId){
        Organization memory org = orgsList[_orgId];
        require(msg.sender == _orgId || msg.sender == org.ent.creatorId || msg.sender == org.adminId || msg.sender == admin, "This function can only be called by the organization, it's creator, it's admin or the system admin. ");
        org.ent.dataHash = _dataHash;
        orgsList[_orgId] = org;
    }
 
    /* Changes the tier of an Organization */
    function setOrganizationTier(address payable _orgId, int _tier) public 
    onlyAdminAnd(_orgId) 
    mustBeOrganization(_orgId){
        Organization memory org = orgsList[_orgId];
        org.ent.tier = _tier;
        orgsList[_orgId] = org;
    }
    
    /* Shows details of Organization as saved on blockchain */
    function viewOrgDetails (address payable _orgId) public view returns (address, int, bytes32, address) {
        return (orgsList[_orgId].ent.uniqueId, orgsList[_orgId].ent.tier,  orgsList[_orgId].ent.dataHash, orgsList[_orgId].adminId);
    }
    
    /* Makes Agent be part of organization */
    function assignAgentToOrganization (address payable _agentId, address payable _orgId) public 
    onlyAdminAnd(orgsList[_orgId].adminId) 
    mustBeAgent(_agentId)
    mustBeOrganization(_orgId) {
        Agent memory agent;
        agent.ent.uniqueId = _agentId;
        agent.orgId = _orgId;

        Organization storage org = orgsList[_orgId];
        org.agentMembers[_agentId] = true;
        orgsList[_orgId] = org;

    }
    
    /* Changes Admin of Organization */
    function changeAdminOfOrganization (address payable _adminId, address payable _orgId) public 
    onlyAddress(orgsList[_orgId].adminId) 
    mustBeAgent(_adminId)
    mustBeOrganization(_orgId) {
        require(validAgents[_adminId] && validOrgs[_orgId]);
        Organization memory org = orgsList[_orgId];
        org.adminId = _adminId;
        orgsList[_orgId] = org;
    }
    
    /* Returns True if Agent _agentId is member of the organization _orgId */
    function isAgentMemberOfOrganization(address payable _agentId, address payable _orgId) public view
    mustBeAgent(_agentId)
    mustBeOrganization(_orgId)
    returns(bool)
    {
        return orgsList[_orgId].agentMembers[_agentId];
    }
    //}
    
    /* ~~~~~~~~~~~~~~~~~~~~~~~~~~~~ DEVICE ~~~~~~~~~~~~~~~~~~~~~~~~~~~~ */
    //{
    /*  Validates address as being of an Organization by adding it to list of valid Orgs. */
    function createNewDevice (address payable _devId, address payable _adminId) public 
    //onlyAdmin() 
    mustBeAgent(_adminId) 
    mustNotBeAgent(_devId)
    mustNotBeDevice(_devId)
    mustNotBeOrganization(_devId){
        Device memory dev;
        dev.ent.uniqueId = _devId;
        dev.adminId = _adminId;
        dev.ent.creatorId = msg.sender;
        devsList[_devId] = dev;
        validDevs[_devId] = true;
    }
    
    /* Check whether address belonngs to a valid Organization */
    function isDevice (address payable _devId) public view returns (bool) {
        return validDevs[_devId];
    }        

    /* Revokes the address' validity as being of a device by removing it from list of Devices. */
    function removeDevice (address payable _devId) public 
    //onlyAdmin() 
    mustBeDevice(_devId){
        validDevs[_devId] = false;
        delete devsList[_devId];
    }
        
    /* Changes the current user of a Device */
    function setDeviceUser (address payable _devId, address payable _userId) public
    mustBeAgent(_userId){
        require (msg.sender == devsList[_devId].adminId, "Unauthorized sender. Must be the owner of the device.");
        Device memory dev = devsList[_devId];
        dev.userId = _userId;
        devsList[_devId] = dev;
    }
 
    /* Changes the current owner of a Device */
    function setDeviceOwner (address payable _devId, address payable _newOwnerId) public
    mustBeAgent(_newOwnerId){
        require (msg.sender == devsList[_devId].adminId, "Unauthorized sender. Must be the owner of the device.");
        Device memory dev = devsList[_devId];
        dev.adminId = _newOwnerId;
        devsList[_devId] = dev;
    }
    //}
}
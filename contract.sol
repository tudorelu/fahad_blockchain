pragma solidity ^0.5.0;

    /**
     * This contract defines three entities - agent, party and device. There 
     * are different tiers of each of these entities - IE agents and parties 
     * can have different importance levels. All these entities interact with 
     * each other, can validate one another and sometimes are inter-depend.
     * 
     * An agent can be simply understood as an individual. The agent's tier
     * gives it it's status. Under any given scenario, different individuals 
     * will have different statuses. For EXAMPLE, for Hospitals, we may have 
     * patients and visitors (Tier 0), nurses (Tier 1) and doctors (Tier 2) 
     * as agents. The tiers define a hierarchy.
     * 
     * A party is simply an entity under which a group of agents operate. 
     * A hospital (Tier 0) might be a party and so might a police station.
     * 
     * Higher-tiered parties are also entities under which both agents and 
     * lower-tiered parties operate - such as a ministry. The Ministry for 
     * Health (Tier 1) should have a minister (Tier 6 agent), lots of public 
     * servants (Tiers 3-5), plus a bunch of hospitals that are recognized 
     * by this Ministry. 
     * 
     * There is a centralized data repository, which contains details about
     * each agent and party. Each entity has access to it's own data. Higher 
     * tiered entities may be able to access some lower tiered entity's data.
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
 * Superclass containing ID details about a generic entity.
 * */
contract Entity {
    
    address payable public  uniqueId;                       // used as a unique id
    int             public  tier;                           // determines the access rights

    constructor (address payable _uniqueId) public {
        uniqueId = _uniqueId;
        tier = 0;
    }
    
    /* sets the tier of this entity */
    function setTier(int _tier) public {
        tier = _tier;
    }
    
}

/**
 * Defines the ID of an individual (person)
 * */
contract Agent is Entity {

    address         public      partyId;                    // address of party of which this agent belongs
    
    constructor(address payable _uniqueId, address _partyId) Entity (_uniqueId) public {
        partyId = _partyId;
    }
}

/**
 * Defines the ID of an organization
 * */
contract Party is Entity {

    address         public      adminId;                    // address of Party admin
    int             public      maxAgentTier;               // max tier of party members
    address         private     _potentialNewAdminId;       // address of potential new admin
    
    constructor(address payable _uniqueId, address _adminId) Entity (_uniqueId) public {
        adminId = _adminId;
        _potentialNewAdminId = address(0);
    }
    
    /*
        Changes the tier level of a given entity
            - must be called by admin
            - newTier must be less than maxAgentTier
    */
    function changeTierLevelOfAgent(Agent _agent, int _newTier) public {
        if(msg.sender != adminId)
            throw;
            
        if(_newTier > maxAgentTier)
            throw;
        
        _agent.setTier(_newTier);
        
    }
    
    /*
        Changes the tier level of a given entity
            - must be called by admin
            - newTier must be less then this Party's tier
    */
    function changeTierLevelOfParty(Party _party, int _newTier) public {
        if(msg.sender != adminId)
            throw;
            
        if(_newTier >= tier)
            throw;
        
        _party.setTier(_newTier);
        
    }
  
    /* 
        Changing the admin of a party is a 2 step process;
        this function constitutes the first step 
    
            - must be called by the current admin
            - with the address of the new admin as parameter
    */
    function initiateAdminChange(address _newAdminId) public {
        if(msg.sender != adminId)
            throw;
        
        _potentialNewAdminId = _newAdminId;
    }
    
    /* 
        Changing the admin of a party is a 2 step process
        this function constitutes the second step 
        
            - must be called by the new admin
    */
    function finalizeAdminChange() public {
        if(msg.sender != _potentialNewAdminId)
            throw;
        
        adminId = _potentialNewAdminId;
        _potentialNewAdminId = address(0);
    }
    
}

/**
 * Defines the ID of an IOT device (a Phone, Sensor, Smart Meter, etc)
 * */
 contract Device is Entity {
    address         public      adminId;        // the address of the device admin (in the case of a hospital, a doctor would own this device and assign it to patients)
    address         public      userId;         // address of the current user of this device (se this device has write access to this user's data)
    
    constructor(address payable _uniqueId, address _adminId) Entity (_uniqueId) public {
        adminId = _adminId;
    }
    
    /*
        Changes the current user of device 
        
        (IE if a patient checks out and another one comes into the same room / bed)
    */
    function changeUser(address _newUser){
        if(msg.sender != adminId)
            throw;
            
        userId = _newUser;
    }
}

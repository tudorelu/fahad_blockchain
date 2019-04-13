/**
 * Defines an organization (institution)
 * 
 * An Organization is simply an entity under which a group of agents operate. 
 * A hospital (Tier 0) might be an Organization and so might a police station.
 * 
 * Higher-tiered Organizations are also entities under which both agents and 
 * lower-tiered Organizations operate - such as a ministry. The Ministry for 
 * Health (Tier 1) should have a minister (Tier 6 agent), lots of public servants 
 * (Tiers 3-5), plus a bunch of hospitals that are recognized by this Ministry. 
 * 
 * */
contract Organization is Entity {

    address         public      adminId;                    // address of Organization admin
    int             public      maxAgentTier;               // max tier of Organization members
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
        Changes the tier level of a given Entity
            - must be called by admin
            - newTier must be less then this Organization's tier
    */
    function changeTierLevelOfOrganization(Party _party, int _newTier) public {
        if(msg.sender != adminId)
            throw;
            
        if(_newTier >= tier)
            throw;
        
        _party.setTier(_newTier);
        
    }
  
    /* 
        Changing the admin of an Organization is a 2 step process;
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
        Changing the admin of an Organization is a 2 step process
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
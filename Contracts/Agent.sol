/**
 * Defines an individual (IE person)
 *
 * An agent can be simply understood as an individual. The agent's tier
 * gives it it's status. Under any given scenario, different individuals 
 * will have different statuses. For EXAMPLE, for Hospitals, we may have 
 * patients and visitors (Tier 0), nurses (Tier 1) and doctors (Tier 2) 
 * as agents. The tiers define a hierarchy.)
 * */
contract Agent is Entity {

    address         public      organizationId;                    // address of Organization of which this Agent belongs
    
    constructor(address payable _uniqueId, address _organizationId) Entity (_uniqueId) public {
        organizationId = _organizationId;
    }
}

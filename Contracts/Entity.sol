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

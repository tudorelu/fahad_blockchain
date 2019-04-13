/**
 * Defines an IOT device (a Phone, Sensor, Smart Meter, etc)
 *
 * It has a permanent administrator (adminId), which temporarily
 * assigns the device to an entity (userId) and in doing so 
 * granting the device write access to some of the entity's data.
 *
 **/

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

pragma solidity ^0.5.0;

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
 contract Interaction { 

    address         admin;

    constructor() {
        admin = msg.sender;
    }
 }
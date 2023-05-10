//SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

contract AlgaeInsurance {
    address public owner;
    uint public premium;
    uint public payout;
    uint public threshold;
    uint public measuredAlgae;
    uint public lastCheck;
    bool public policyActive;
    bool public bloom;
    mapping(address => uint) public policyholderBalance;
    address payable[] policyholders;

    constructor(uint _premium, uint _payout, uint _threshold) payable {
        owner = payable(msg.sender);
        premium = _premium;
        payout = _payout;
        threshold = _threshold;
        lastCheck = block.timestamp;
        policyActive = true;
        bloom = false;
    }

    function buyPolicy() public payable {
        require(policyActive == true, "Policy is not active");
        require(msg.value == premium, "Incorrect premium amount");
        policyholderBalance[msg.sender] = msg.value;
        policyholders.push(payable(msg.sender));
    }

    // setting test values for measured algae and the threshold for a bool+
    function testContractWith(uint _testThreshold, uint _testMeasured) public {
        require(msg.sender == owner, "Only the owner sets these params");
        threshold = _testThreshold;
        measuredAlgae = _testMeasured;
        //checkAlgaeBloom();
    }

    function checkAlgaeBloom() public returns (bool) {
        require(
            msg.sender == owner,
            "Only the owner can trigger this function"
        );
        // Use satellite data to analyze the presence and intensity of algae blooms
        // If the threshold is exceeded, trigger payout and deactivate policy
        // Code to check satellite data and determine bloom status

        // measuredAlgae is the simulated oracle response for testing
        bloom = measuredAlgae > threshold;
        if (bloom == true) {
            for (uint i = 0; i < policyholders.length; i++) {
                payable(policyholders[i]).transfer(payout);
            }
            policyActive = false;
            return true;
        }
        return false;
    }

    function closePolicy() public {
        require(msg.sender == owner, "Only the owner can close the policy");
        policyActive = false;
        for (uint i = 0; i < policyholders.length; i++) {
            payable(policyholders[i]).transfer(
                policyholderBalance[policyholders[i]]
            );
            policyholderBalance[policyholders[i]] = 0;
        }
    }

    function getPolicyholderByIndex(uint _index) public view returns (address) {
        return policyholders[_index];
    }

    function getPolicyBalance(
        address _policyHolder
    ) public view returns (uint) {
        return policyholderBalance[_policyHolder];
    }

    function depositFunds() public payable returns (uint) {
        // require(msg.sender == owner, "Only the owner can deposit funds");
        return msg.value;
    }

    function activatePolicy() public {
        require(msg.sender == owner, "Only the owner can activate this policy");
        policyActive = true;
        bloom = false;
    }
}

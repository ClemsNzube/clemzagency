// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract PropertyRental {
    address public owner;
    struct Property {
        uint256 id;
        address payable agent;
        string title;
        string location;
        uint256 price;
        bool isRented;
    }

    mapping(uint256 => Property) public properties;

    event PropertyRented(uint256 propertyId, address renter);

    constructor() public {  // Constructor visibility added
        owner = msg.sender;
    }

    function addProperty(
        uint256 id,
        address payable agent,
        string memory title,
        string memory location,
        uint256 price
    ) public {
        require(msg.sender == owner, "Only the owner can add properties.");
        properties[id] = Property(id, agent, title, location, price, false);
    }

    function rentProperty(uint256 propertyId) public payable {
        Property storage property = properties[propertyId];
        require(!property.isRented, "Property is already rented.");
        require(msg.value >= property.price, "Insufficient funds.");

        property.agent.transfer(msg.value);
        property.isRented = true;

        emit PropertyRented(propertyId, msg.sender);
    }

    function getProperty(uint256 propertyId)
        public
        view
        returns (
            address agent,
            string memory title,
            string memory location,
            uint256 price,
            bool isRented
        )
    {
        Property memory property = properties[propertyId];
        return (
            property.agent,
            property.title,
            property.location,
            property.price,
            property.isRented
        );
    }
}

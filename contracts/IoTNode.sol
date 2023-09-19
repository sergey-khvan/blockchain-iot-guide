// SPDX-License-Identifier: Sergey Khvan
pragma solidity ^0.8.0;

contract IoTNode {
    struct SensorReading {
        uint256 timestamp;
        uint256 value;
    }

    mapping(address => SensorReading[]) public readings;

    function addReading(uint256 _value) public {
        SensorReading memory reading = SensorReading(block.timestamp, _value);
        readings[msg.sender].push(reading);
    }

    function getReadingCount(address _owner) public view returns (uint256) {
        return readings[_owner].length;
    }

    function getReading(address _owner, uint256 _index) public view returns (uint256, uint256) {
        require(_index < readings[_owner].length, "Invalid index");
        SensorReading storage reading = readings[_owner][_index];
        return (reading.timestamp, reading.value);
    }
}
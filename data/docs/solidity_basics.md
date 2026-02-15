# Solidity Basics

## What is Solidity?
Solidity is a statically-typed, contract-oriented programming language designed for developing smart contracts on the Ethereum blockchain. It was influenced by C++, Python, and JavaScript. Solidity is the most popular language for writing Ethereum smart contracts.

## What is a Smart Contract?
A smart contract is a self-executing program stored on a blockchain that automatically enforces the terms of an agreement when predetermined conditions are met. Smart contracts eliminate the need for intermediaries, reducing costs and increasing transparency.

### Key Characteristics:
- **Immutable**: Once deployed, the code cannot be changed
- **Deterministic**: Same input always produces same output
- **Decentralized**: Runs on the blockchain network, not a single server
- **Transparent**: Code is visible to everyone on the blockchain
- **Self-executing**: Automatically executes when conditions are met

## Basic Structure of a Solidity Contract

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract MyFirstContract {
    // State variables
    uint256 public myNumber;
    string public myString;
    address public owner;

    // Constructor - runs once when contract is deployed
    constructor() {
        owner = msg.sender;
        myNumber = 0;
    }

    // Function to set a number
    function setNumber(uint256 _number) public {
        myNumber = _number;
    }

    // Function to get the number
    function getNumber() public view returns (uint256) {
        return myNumber;
    }
}
```

## Data Types in Solidity

### Value Types:
- **bool**: true or false
- **uint**: Unsigned integers (uint8 to uint256)
- **int**: Signed integers (int8 to int256)
- **address**: Holds a 20-byte Ethereum address
- **bytes**: Fixed-size byte arrays (bytes1 to bytes32)

### Reference Types:
- **string**: Dynamic-size UTF-8 encoded string
- **bytes**: Dynamic-size byte array
- **arrays**: Fixed or dynamic size arrays
- **mapping**: Key-value hash tables
- **struct**: Custom defined structures

## Storage vs Memory vs Calldata

- **Storage**: Permanent data stored on the blockchain. State variables are storage by default. Expensive to use (costs gas).
- **Memory**: Temporary data that exists during function execution. Function parameters and local variables of reference types use memory. Cheaper than storage.
- **Calldata**: Read-only temporary data. Similar to memory but immutable. Used for external function parameters. Most gas efficient for read-only data.

```solidity
contract StorageExample {
    uint256[] public numbers; // storage by default

    function example(uint256[] calldata input) external {
        // input is calldata (read-only, cheapest)
        uint256[] memory tempArray = new uint256[](input.length); // memory (temporary)
        numbers = input; // copies to storage (permanent, expensive)
    }
}
```

## Visibility Modifiers

- **public**: Can be called internally and externally. Automatically creates a getter for state variables.
- **private**: Only accessible within the contract that defines it.
- **internal**: Accessible within the contract and derived contracts.
- **external**: Can only be called from outside the contract. Cannot be called internally (except with `this.functionName()`).

## Function Modifiers

```solidity
contract ModifierExample {
    address public owner;

    constructor() {
        owner = msg.sender;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Not the owner");
        _; // Continue executing the function
    }

    function sensitiveAction() public onlyOwner {
        // Only the owner can call this
    }
}
```

## Events

Events allow logging to the Ethereum blockchain. They are useful for notifying external applications about contract state changes.

```solidity
contract EventExample {
    event Transfer(address indexed from, address indexed to, uint256 amount);

    function transfer(address to, uint256 amount) public {
        // ... transfer logic ...
        emit Transfer(msg.sender, to, amount);
    }
}
```

## Gas and Gas Optimization

Gas is the unit of computation on Ethereum. Every operation costs gas. Key optimization tips:
- Use `uint256` instead of smaller uint types (EVM operates on 256-bit words)
- Pack struct variables to save storage slots
- Use `calldata` instead of `memory` for read-only function parameters
- Use events instead of storing data when historical data is needed
- Minimize storage operations (most expensive)
- Use `immutable` and `constant` keywords for values that don't change

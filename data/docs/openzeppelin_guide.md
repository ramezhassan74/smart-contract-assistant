# OpenZeppelin Smart Contract Guide

## What is OpenZeppelin?
OpenZeppelin is the most widely used library for secure smart contract development on Ethereum and other EVM-compatible blockchains. It provides tested, community-reviewed implementations of ERC standards and common patterns.

## Installation
```bash
npm install @openzeppelin/contracts
```

## ERC-20 Token Standard

ERC-20 is the standard interface for fungible tokens on Ethereum.

### Basic ERC-20 Token:
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract MyToken is ERC20 {
    constructor(uint256 initialSupply) ERC20("MyToken", "MTK") {
        _mint(msg.sender, initialSupply * 10 ** decimals());
    }
}
```

### ERC-20 with Access Control and Minting:
```solidity
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract MyToken is ERC20, Ownable {
    constructor() ERC20("MyToken", "MTK") Ownable(msg.sender) {
        _mint(msg.sender, 1000000 * 10 ** decimals());
    }

    function mint(address to, uint256 amount) public onlyOwner {
        _mint(to, amount);
    }
}
```

## ERC-721 NFT Standard

ERC-721 is the standard for non-fungible tokens (NFTs).

### Basic NFT Contract:
```solidity
import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract MyNFT is ERC721, ERC721URIStorage, Ownable {
    uint256 private _nextTokenId;

    constructor() ERC721("MyNFT", "MNFT") Ownable(msg.sender) {}

    function safeMint(address to, string memory uri) public onlyOwner {
        uint256 tokenId = _nextTokenId++;
        _safeMint(to, tokenId);
        _setTokenURI(tokenId, uri);
    }

    // Required overrides
    function tokenURI(uint256 tokenId)
        public view override(ERC721, ERC721URIStorage) returns (string memory)
    {
        return super.tokenURI(tokenId);
    }

    function supportsInterface(bytes4 interfaceId)
        public view override(ERC721, ERC721URIStorage) returns (bool)
    {
        return super.supportsInterface(interfaceId);
    }
}
```

## ERC-1155 Multi Token Standard

ERC-1155 allows a single contract to manage multiple token types (both fungible and non-fungible).

```solidity
import "@openzeppelin/contracts/token/ERC1155/ERC1155.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract GameItems is ERC1155, Ownable {
    uint256 public constant GOLD = 0;
    uint256 public constant SILVER = 1;
    uint256 public constant SWORD = 2;

    constructor() ERC1155("https://game.example/api/item/{id}.json") Ownable(msg.sender) {
        _mint(msg.sender, GOLD, 10**18, "");
        _mint(msg.sender, SILVER, 10**27, "");
        _mint(msg.sender, SWORD, 1, "");
    }
}
```

## Access Control

### Ownable:
Simple single-owner access control.
```solidity
import "@openzeppelin/contracts/access/Ownable.sol";

contract MyContract is Ownable {
    constructor() Ownable(msg.sender) {}

    function restrictedFunction() public onlyOwner {
        // Only owner can call
    }
}
```

### AccessControl (Role-Based):
More flexible role-based access control.
```solidity
import "@openzeppelin/contracts/access/AccessControl.sol";

contract MyContract is AccessControl {
    bytes32 public constant MINTER_ROLE = keccak256("MINTER_ROLE");
    bytes32 public constant PAUSER_ROLE = keccak256("PAUSER_ROLE");

    constructor() {
        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _grantRole(MINTER_ROLE, msg.sender);
    }

    function mint(address to) public onlyRole(MINTER_ROLE) {
        // Only addresses with MINTER_ROLE can call
    }
}
```

## Upgradeable Contracts

OpenZeppelin provides proxy patterns for upgradeable contracts.

### Transparent Proxy Pattern:
```solidity
import "@openzeppelin/contracts-upgradeable/proxy/utils/Initializable.sol";
import "@openzeppelin/contracts-upgradeable/token/ERC20/ERC20Upgradeable.sol";

contract MyTokenV1 is Initializable, ERC20Upgradeable {
    function initialize(string memory name, string memory symbol) public initializer {
        __ERC20_init(name, symbol);
        _mint(msg.sender, 1000000 * 10 ** decimals());
    }
}
```

## Pausable Contracts

Allow authorized users to pause contract functionality in emergencies.

```solidity
import "@openzeppelin/contracts/security/Pausable.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract MyContract is Pausable, Ownable {
    constructor() Ownable(msg.sender) {}

    function normalOperation() public whenNotPaused {
        // Can only be called when not paused
    }

    function pause() public onlyOwner {
        _pause();
    }

    function unpause() public onlyOwner {
        _unpause();
    }
}
```

## ReentrancyGuard

Protects against reentrancy attacks.

```solidity
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

contract MyContract is ReentrancyGuard {
    mapping(address => uint256) public balances;

    function withdraw() public nonReentrant {
        uint256 amount = balances[msg.sender];
        balances[msg.sender] = 0;
        (bool success, ) = msg.sender.call{value: amount}("");
        require(success);
    }
}
```

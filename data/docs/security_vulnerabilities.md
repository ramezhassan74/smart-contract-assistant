# Smart Contract Security Vulnerabilities

## 1. Reentrancy Attack

Reentrancy is one of the most dangerous vulnerabilities in smart contracts. It occurs when a contract makes an external call to another contract before updating its own state, allowing the called contract to re-enter the calling contract and exploit the outdated state.

### The Famous DAO Hack
The DAO hack in 2016 exploited a reentrancy vulnerability, resulting in the loss of approximately 3.6 million ETH (around $60 million at the time).

### Vulnerable Code Example:
```solidity
// VULNERABLE - DO NOT USE
contract VulnerableBank {
    mapping(address => uint256) public balances;

    function deposit() public payable {
        balances[msg.sender] += msg.value;
    }

    function withdraw() public {
        uint256 balance = balances[msg.sender];
        require(balance > 0, "No balance");

        // BUG: External call before state update
        (bool success, ) = msg.sender.call{value: balance}("");
        require(success, "Transfer failed");

        // State update happens AFTER the external call
        balances[msg.sender] = 0;
    }
}
```

### Attack Contract:
```solidity
contract Attacker {
    VulnerableBank public bank;

    constructor(address _bankAddress) {
        bank = VulnerableBank(_bankAddress);
    }

    function attack() external payable {
        bank.deposit{value: msg.value}();
        bank.withdraw();
    }

    receive() external payable {
        if (address(bank).balance >= 1 ether) {
            bank.withdraw(); // Re-enters withdraw before balance is set to 0
        }
    }
}
```

### Prevention - Checks-Effects-Interactions Pattern:
```solidity
contract SecureBank {
    mapping(address => uint256) public balances;

    function withdraw() public {
        uint256 balance = balances[msg.sender];
        require(balance > 0, "No balance");

        // Effect: Update state BEFORE making external call
        balances[msg.sender] = 0;

        // Interaction: External call AFTER state update
        (bool success, ) = msg.sender.call{value: balance}("");
        require(success, "Transfer failed");
    }
}
```

### Prevention - Using ReentrancyGuard:
```solidity
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

contract SecureBank is ReentrancyGuard {
    mapping(address => uint256) public balances;

    function withdraw() public nonReentrant {
        uint256 balance = balances[msg.sender];
        require(balance > 0, "No balance");
        balances[msg.sender] = 0;
        (bool success, ) = msg.sender.call{value: balance}("");
        require(success, "Transfer failed");
    }
}
```

## 2. Integer Overflow and Underflow

Before Solidity 0.8.0, arithmetic operations could overflow or underflow without throwing an error.

```solidity
// In Solidity < 0.8.0
uint8 max = 255;
max + 1; // Would wrap around to 0 (overflow)

uint8 min = 0;
min - 1; // Would wrap around to 255 (underflow)
```

### Prevention:
- Use Solidity 0.8.0+ which has built-in overflow checks
- Use OpenZeppelin's SafeMath library for older versions

```solidity
// SafeMath for Solidity < 0.8.0
import "@openzeppelin/contracts/utils/math/SafeMath.sol";

contract SafeExample {
    using SafeMath for uint256;

    function safeAdd(uint256 a, uint256 b) public pure returns (uint256) {
        return a.add(b); // Will revert on overflow
    }
}
```

## 3. Access Control Issues

Failing to properly restrict access to sensitive functions.

```solidity
// VULNERABLE
contract VulnerableContract {
    address public owner;

    // Anyone can call this!
    function changeOwner(address newOwner) public {
        owner = newOwner;
    }
}

// SECURE
contract SecureContract {
    address public owner;

    constructor() {
        owner = msg.sender;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Not authorized");
        _;
    }

    function changeOwner(address newOwner) public onlyOwner {
        require(newOwner != address(0), "Invalid address");
        owner = newOwner;
    }
}
```

## 4. Front-Running

Front-running occurs when a malicious actor observes a pending transaction in the mempool and submits their own transaction with a higher gas price to get it executed first.

### Prevention:
- Use commit-reveal schemes
- Use submarine sends
- Implement batch auctions
- Use private mempools or Flashbots

## 5. Denial of Service (DoS)

### DoS with Block Gas Limit:
```solidity
// VULNERABLE - could run out of gas with many users
contract VulnerableAirdrop {
    function distribute(address[] memory recipients, uint256 amount) public {
        for (uint i = 0; i < recipients.length; i++) {
            payable(recipients[i]).transfer(amount);
        }
    }
}

// SECURE - use pull pattern instead
contract SecureAirdrop {
    mapping(address => uint256) public pendingWithdrawals;

    function distribute(address[] memory recipients, uint256 amount) public {
        for (uint i = 0; i < recipients.length; i++) {
            pendingWithdrawals[recipients[i]] += amount;
        }
    }

    function withdraw() public {
        uint256 amount = pendingWithdrawals[msg.sender];
        pendingWithdrawals[msg.sender] = 0;
        payable(msg.sender).transfer(amount);
    }
}
```

## 6. Tx.origin Authentication

Never use `tx.origin` for authentication. Use `msg.sender` instead.

```solidity
// VULNERABLE
function transfer(address to, uint256 amount) public {
    require(tx.origin == owner); // Can be exploited via phishing
}

// SECURE
function transfer(address to, uint256 amount) public {
    require(msg.sender == owner); // Correct way
}
```

## Security Best Practices Checklist

1. Follow the Checks-Effects-Interactions pattern
2. Use ReentrancyGuard for functions that make external calls
3. Use Solidity 0.8.0+ for built-in overflow protection
4. Implement proper access control (OpenZeppelin AccessControl)
5. Avoid using tx.origin for authentication
6. Use pull over push for payments
7. Be careful with delegatecall
8. Always validate inputs
9. Use established libraries (OpenZeppelin)
10. Get professional audits before deploying to mainnet

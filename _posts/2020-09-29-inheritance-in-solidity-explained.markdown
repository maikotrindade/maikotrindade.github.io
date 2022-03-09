---
published: true
title: Inheritance in Solidity explained
layout: post
---


### Intro

Solidity supports multiple inheritance including polymorphism. Inheritance is the process of defining multiple contracts that are related to each other through parent-child relationships. The contract that is inherited is called the parent contract and the contract that inherits is called the child contract. 

When a contract inherits from other contracts, only a single contract is created on the blockchain, and the code from all the base contracts is compiled into the created contract. This means that all internal calls to functions of base contracts also just use internal function calls.

The benefits of using inheritance are: Ability to change one contract and have those modifications reflected in others, Reducement of dependency nad Ability to reuse existing code more.

### Example of Inheritance

```
pragma solidity ^0.8.0;

contract Grandparent {
    function myFunction() public pure virtual returns (string memory) {
        return "Contract Grandparent";
    }
}

// Contracts inherit other contracts by using the keyword 'is'.
contract Parent is Grandparent {
    // Override Grandparent.myFunction()
    function myFunction() public pure virtual override returns (string memory) {
        return "Contract Parent";
    }
}

contract Uncle is Grandparent {
    // Override Grandparent.myFunction()
    function myFunction() public pure virtual override returns (string memory) {
        return "Contract Uncle";
    }
}
```

*Note:* Solidity copies the base contracts into the derived contract and a single contract is created with inheritance. A single address is generated that is shared between contracts in a parent-child relationship.



### 💡 Gotchas

- In the case of multiple inheritances, function calls using super gives preference to most derived contracts;
- There are different types of inheritances: Single, Multi-level, Multiple and Hierarchical;
- A derived contract can access all non-private members including state variables and internal methods. But using this is not allowed;
- We can call a super contract’s function using a `super` keyword or using a super contract name;


 
### Additional Information
	
[Inheritance in Solidity] – Solidity docs

[Inheritance in Solidity]: https://docs.soliditylang.org/en/v0.6.2/contracts.html#inheritance



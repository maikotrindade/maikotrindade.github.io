---
published: true
title: Hello Solidity, hello Ethereum
layout: post
---

According to [official Solidity docs] is a contract-oriented, Solidity is a high-level language for implementing smart contracts. It was influenced by C++,
Python and JavaScript and is designed to target the Ethereum Virtual Machine (EVM).

Alright, let's talk about Solidity' syntax and its features. Basically I'm mention the following subjects: Contracts, Types of variables, Math operations, Functions, Arrays, Structs and Events. 

#### Let's start 

A contract is the fundamental building block of Ethereum applications — everything goes inside the contracts. This is very similar to Java, commonly all the code is encapsuled in 'Class'.  

First important thing you need to learn is how Solidity handles variables. Solidity is a statically typed language, which means that the type of each variable. Once you start coding variables and functions inside you Contract file, you need to understand Solidity has two types of variables: state and local. 
State variables are permanently stored in contract storage - into the Ethereum blockchain, it may cost some 'gas' in case you try to modify them.
Local variable you can modify them freely but remember you will loose their value right after the context/scope change - they are not stored.  

**Booleans**
`bool`: The possible values are constants true and false.

**Integers**
`int` / `uint`: Signed and unsigned integers of various sizes. Keywords uint8 to uint256 in steps of 8 (unsigned of 8 up to 256 bits) and int8 to int256. uint and int are aliases for uint256 and int256, respectively.

**Address**
`address`: Holds a 20 byte value (size of an Ethereum address). Address types also have members and serve as a base for all contracts.

**Members of Addresses**
`balance` and `transfer`: It is possible to query the balance of an address using the property balance and to send Ether (in units of wei) to an address using the transfer function.

**Fixed-size byte arrays**
`bytes1`, `bytes2`, `bytes3`, …, `bytes32`. byte is an alias for `bytes1`.

**Dynamically-sized byte array**
bytes: Dynamically-sized byte array.
string: Dynamically-sized UTF-8-encoded string.

**String Literals**
They are written with either double or single-quotes ("foo" or 'bar'). They do not imply trailing zeroes as in C; "foo" represents three bytes not four. As with integer literals, their type can vary, but they are implicitly convertible to bytes1, …, bytes32, if they fit, to bytes and to string.

#### Math Operations

Solidity offers the following math operations (it is almost the same as in most programming languages):

Addition: x + y
Subtraction: x - y,
Multiplication: x * y
Division: x / y
Modulus / remainder: x % y 
Support an exponential operator (i.e. "x to the power of y", x^y):

#### Structs
Sometimes you need a more complex data type. For this, Solidity provides structs:

`struct Person {
  uint age;
  string name;
}
Structs allow you to create more complicated data types that have multiple properties.

#### Events
Events are a way for your contract to communicate that something happened on the blockchain to your app front-end, which can be 'listening' for certain events and take action when they happen.

[Events] are inheritable members of contracts. When they are called, they cause the arguments to be stored in the transaction’s log - a special data structure in the blockchain. These logs are associated with the address of the contract and will be incorporated into the blockchain and stay there as long as a block is accessible (forever as of Frontier and Homestead, but this might change with Serenity). Log and event data is not accessible from within contracts (not even from the contract that created them).


#### Further details 

I'd recommend this article [Ethereum Smart Contract Best Practices] for beginners.

[official Solidity docs]: https://media.readthedocs.org/pdf/solidity/develop/solidity.pdf
[Events]: https://github.com/ethereum/wiki/wiki/JavaScript-API#contract-events
[Ethereum Smart Contract Best Practices]: https://consensys.github.io/smart-contract-best-practices/recommendations/ 
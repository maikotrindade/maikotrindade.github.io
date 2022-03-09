---
published: true
title: How is the structure of a smart contract
layout: post
---


Smart contracts are the basic unit of deployment and execution for EVMs. A contract contains state variables, functions, function modifiers, events, structures, and enums. Contracts also support inheritance. Inheritance is implemented by copying code at the time of compiling. Smart contracts also support polymorphism.

Every transaction on Ethereum Virtual Machine costs us some amount of Gas. The lower the Gas consumption the better is your Solidity code. The Gas consumption of Memory is not very significant as compared to the gas consumption of Storage. Therefore, it is always better to use Memory for intermediate calculations and store the final result in Storage.

 
### State variables

The variable can be used at multiple places within code and they will all refer to the value stored within it. Solidity provides two types of variable: *state and memory*. 

The default for function parameters (including return parameters of functions) is *memory*, the default for local variables is storage.


### Storage

Persistent data is referred to as storage and is represented by state variables. These values get stored permanently on the blockchain. You need to declare the type so that the contract can keep track of how much storage on the blockchain it needs when it compiles.


### Structure 
Structures or structs helps implement custom user-defined data types. A structure is a composite data type, consisting of multiple variables of different data types. They are very similar to contracts; however, they do not contain any code within them. They consist of only variables.
	
[ANATOMY OF SMART CONTRACTS] by Ethereum.org

[ANATOMY OF SMART CONTRACTS]: https://ethereum.org/en/developers/docs/smart-contracts/anatomy/



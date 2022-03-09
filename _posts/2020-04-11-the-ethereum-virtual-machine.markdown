---
published: true
title: EVM – Ethereum Virtual Machine 
layout: post
---


### Intro

Solidity is a programming language targeting Ethereum Virtual Machine (EVM). 
Ethereum blockchain helps extend its functionality by writing and executing code known as smart contracts. Ethereum Virtual Machines have been successfully implemented in various programming languages including C++, Java, JavaScript, Python, Ruby, and many others.

EVM executes code that is part of smart contracts. Smart contracts are written in Solidity; however, EVM does not understand the high-level constructs of Solidity. EVM understands lower-level instructions called bytecode. Solidity code needs a compiler to take its code and convert it into bytecode that is understandable by EVM.

For every instruction implemented on the EVM, a system that keeps track of execution cost, assigns to the instruction an associated cost in Gas units (See our What is Gas? article). When a user wants to initiate an execution, they reserve some Ether, which they are willing to pay for this gas cost.

In order to facilitate Keccak-256 cryptographic hash scheme, the EVM is a stack-based architecture with a word size of 256-bits. This architecture also allows for the use of elliptic-curve cryptography in Ethereum's signature scheme for validating the origin and integrity of transactions.

<img src="http://maikotrindade.github.io/public/img/evm.png" width="580" height="340" alt="EVM"/>


### Additional Information
	
[ETHEREUM VIRTUAL MACHINE (EVM)] by Ethereum.org

[ETHEREUM VIRTUAL MACHINE (EVM)]: https://ethereum.org/en/developers/docs/evm/



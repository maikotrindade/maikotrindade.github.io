---
published: true
title: Solidity – Call x Transactions and Solidity functions
layout: post
---

In [Ethereum], it is possible to interact with contracts via calls (_aka message calls_) or via transactions.
The [official documentation] says:

### Transaction
> A piece of data, signed by an External Actor. It represents either a Message or a new Autonomous Object. Transactions are recorded into each block of the blockchain.

### Message Call
> The act of passing a message from one Account to another. If the destination account is associated with non-empty EVM Code, then the VM will be started with the state of said Object and the Message acted upon. If the message sender is an Autonomous Object, then the Call passes any data returned from the VM operation.
  
In other words, a **transaction** is an asynchronous operation which is broadcasted to the network and processed by miners. A transaction consumes Ether and modify the blockchain. A **message call** is a read-only and not Ether consumer operation of a contract function. The results of a 'call' will not be published or broadcasted on the blockchain.

## Modifiers and Visibility

### Solidity Modifiers
Since [Solidity 0.4.17], it provides the following functions modifiers on its framework: `view` and `pure`.

**View** – should be used in functions that did not change any state values of a contract;  

**Pure** – should be used if it does not even read any state information. Pure functions can be used for tasks like permission-control, calculations and typecasting.

### Visibility

**public** – are part of the contract interface and can be either called internally or via messages. For public state variables, an automatic getter function (see below) is generated;  

**private** – and state variables are only visible for the contract they are defined in and not in derived contracts;  

**internal** – and state variables can only be accessed internally (i.e. from within the current contract or contracts deriving from it), without using `this`;  

**external** – are part of the contract interface, which means they can be called from other contracts and via transactions. An external function `f` cannot be called internally (i.e. `f()` does not work, but `this.f()` works). External functions are sometimes more efficient when they receive large arrays of data;


[Ethereum]: https://www.ethereum.org/
[Solidity]: http://solidity.readthedocs.io
[official documentation]: https://ethereum.github.io/yellowpaper/paper.pdf
[Solidity 0.4.17]: https://github.com/ethereum/solidity/releases/tag/v0.4.17
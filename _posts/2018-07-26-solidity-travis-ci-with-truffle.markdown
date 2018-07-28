---
published: true
title: Solidity – Gas, gas price, fee and gas usage
layout: post
---

**gas** – is the name for a special unit used in Ethereum

**gas price** – a value set by the creator of the transaction; it's a single gas unit's price;

**fee** – the result of  **gas** * **gas price**

### Transactions costs x [Ethereum] system 

* Have in mind if the gas price is too low, no one will process your transaction;

* The fees are paid in ether, though, which is different from gas; 

* The transaction fails (still goes into the blockchain) in case of gas price is fine but the gas cost runs "over budget". You don't get the money back for the work that the miners did.

* Transaction fee = Amount of work that goes into something + storage space your code will take;

### Optimize gas usage of your smart contract

Gas is necessary for the execution of smart contracts, but you shouldn't specify too low or high price. Consider optimizing your smart contract to minimize the amount of gas required.

#### What should I take into account for optimized contracts?  

**Global Variables usage – storage**: Global variables are stored in a contract’s state on the blockchain, so you are going to be charged if you use global variables. Just use when it is necessary, this is a  practice in several languages, but it is especially crucial in ethereum development;    

**Contract Size**: The size of your contract will influence the transaction cost for all interactions with it. So how big is your contract, more expansive your contract will be to processed in the Ethereum's network. If you are able to break the [Solidity] contract up into smaller separate contracts, this will decrease user’s gas costs;   
  
#### Further Details
Take a look in this [documentation from ConsenSys] for Ethereum Smart Contract Security Best Practices and this [Medium post] about Optimizing gas usage.


[Ethereum]: https://www.ethereum.org/
[Solidity]: http://solidity.readthedocs.io
[documentation from ConsenSys]: https://consensys.github.io/smart-contract-best-practices/
[Medium post]: https://medium.com/coinmonks/optimizing-your-solidity-contracts-gas-usage-9d65334db6c7
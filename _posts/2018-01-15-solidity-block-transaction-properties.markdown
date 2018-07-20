---
published: true
title: Solidity – Block and Transaction Properties
layout: post
---

[Solidity] provides special variables and functions which always exist in the global namespace and are mainly used to provide information about the blockchain or are general-use utility functions. The following is a list of properties related to the block and transactions:


•	 **block.blockhash** (uint blockNumber) returns (bytes32): Hash of the given block, works for only the 256 most recent blocks  
•	 **block.coinbase** (address): Current block miner’s address  
•	 **block.difficult** (uint): Current block difficulty  
•	 **block.gaslimit** (uint): Current block gas limit  
•	 **block.number** (uint): Current block number  
•	 **block.timestamp** (uint): Current block timestamp  
•	 **msg.data** (bytes): Complete call data  
•	 **msg.gas** (uint): Remaining gas  
•	 **msg.sender** (address): Sender of the message (current call)  
•	 **msg.sig** (bytes4): First 4 bytes of the call data (function identifier)  
•	 **msg.value** (uint): Number of wei sent with the message  
•	 **now** (uint): Current block timestamp (alias for block.timestamp)  
•	 **tx.gasprice** (uint): Gas price of the transaction  
•	 **tx.origin** (address): Sender of the transaction (full call chain)  


[Solidity]: http://solidity.readthedocs.io
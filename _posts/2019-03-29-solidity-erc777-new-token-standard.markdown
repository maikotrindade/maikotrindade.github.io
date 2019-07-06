---
published: true
title: How to start with the new token standard ERC777 with Solidity
layout: post
---

### Introduction

[ERC20] is a standard which defines a common list of rules that an Ethereum token has to implement, giving developers the ability to program how new tokens will function within the Ethereum ecosystem. [ERC20] defines how the tokens are transferred between addresses and how data within each token is accessed.

The [ERC777] token standard specifies an improvement of [ERC20] while remaining backward compatible. It defines advanced features to interact with tokens. Namely, operators to send tokens on behalf of another address—contract or regular account—and send/receive hooks to offer token holders more control over their tokens.

### ERC777 in a nutshell

Transactions – Let's talk about of the most interesting features that this new standard is bringing to the world. [ERC777] has a function called `send()` consists in having a transaction with an amount field and a data bit field. Thus the parameters can be freely selected again by the token user and the token operator in order to forward data to the recipient.

`
	function send(address to, uint256 amount, bytes calldata data) external;
	    function operatorSend(
	        address from,
	        address to,
	        uint256 amount,
	        bytes calldata data,
	        bytes calldata operatorData
	    ) external;
`


Burning Tokens – [ERC777] provides a feature called "Burning tokens". It is the act of destroying existing tokens that explicitly defines two functions to burn tokens (`burn` and `operatorBurn`). These functions facilitate the integration of the burning process in wallets and dapps. However, the token contract may prevent some or all holders from burning tokens for any reason. The token contract may also define other functions to burn tokens.

Backward Compatibility – The standard does not use `transfer` and `transferFrom` and uses `send` and `operatorSend` to avoid confusion and mistakes when deciphering which token standard is being used. Besides, [ERC777] allows the implementation of ERC20 functions transfer, transferFrom, approve and allowance alongside to make a token fully compatible with [ERC20].

### Reference Implementation - getting started 

I would suggest two references: 
1. [0xjac]
2. [OpenZeppelin]

#### 0xjac

This repository contains all reference implementation and all tests. The reference implementation is also available via npm. In order to use it, you can download and setup the npm in your machine, access the [npm website] to see the instructions.

After the npm configuration, install the erc777 with:

`npm install erc777`

#### OpenZeppelin

OpenZeppelin is an open framework of reusable and secure smart contracts in the Solidity. It provides implementations of standards like ERC20, ERC721 and now ERC777 too. The project started providing [ERC777] after implementing the [issue-1159]. 

In this contract `ERC777.sol`, we can see how the ERC777 implementation are being organized. The contract implements the interface `IERC777` and `IERC20`, it is possible to safely interact with ERC22 and ERC777 while all the events are emitted during the interactions.


In order to use the OpenZeppelin implementation in your project, you can download and setup the npm in your machine, access the [npm website] to see the instructions.

After the npm configuration, install the openzeppelin with:

`npm install openzeppelin-solidity`

### Further details

See [ERC777: a New Advanced Token Standard] by Jordi Baylina, ERC777's author, along Jacques Dafflon and Thomas Shababi

[ERC777]: https://github.com/ethereum/EIPs/issues/777
[ERC20]: https://github.com/ethereum/EIPs/issues/20
[0xjac]: https://github.com/0xjac/ERC777
[OpenZeppelin]: https://docs.openzeppelin.org/v2.3.0/api/token/erc777
[npm website]: https://www.npmjs.com/get-npm
[issue-1159]: https://github.com/OpenZeppelin/openzeppelin-solidity/issues/1159
[ERC777.sol]: https://github.com/OpenZeppelin/openzeppelin-solidity/blob/master/contracts/token/ERC777/ERC777.sol
[ERC777: a New Advanced Token Standard]: https://www.youtube.com/watch?v=CVdZ09iqQj8
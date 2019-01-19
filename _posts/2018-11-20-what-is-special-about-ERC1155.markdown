---
published: true
title: What is special about ERC1155?
layout: post
---

According to Blockchain experts, Non-Fungible Tokens can revolutionize the future of blockchain. Do you really understand this concept and how can it be used? Let’s start talking about the basics and discussing what makes NFTs special and with a promising future.

### Fungible Tokens and Non Fungible Tokens
Fungibility is important in the world of blockchain and cryptocurrency. It is desired for any currency, traditional or digital, since most currencies aim to be an interchangeable asset. A token can be exchanged for any other token of the same value. For example, One US dollar currency can be changed for another US dollar currency without any difference to the user.

On the other hand, Non-Fungible Token can’t be exchanged for any other NFT, because it has a unique and non-interchangeable behavior. These characteristics make them different from each other and digitally scarce. It is possible to create an analogy of NFTs with opera show tickets. Although the tickets are for the same show and everyone will listen to the same songs, each ticket has an identifier, buyer’s name and seat number. They are not easily transferable because each ticket has its value in a unique way.

In the Ethereum network, there are popular patterns that have been specified by the community itself. Each standard is known as ERC which stands for Ethereum Request for Comments. It defines methods, technology, behaviors for a particular functionality in Ethereum and it is submitted either for peer review.


<img src="http://maikotrindade.github.io/public/img/nonfungibletable.png" width="580" height="230" alt="ERC20 compared with ERC721"/>

### ERC-1155
ERC-1155 is a standard for contracts that manage any combination of fungible tokens and non-fungible tokens.

Let’s talk about how the management works in every mentioned pattern in this article. Each ERC-20 token is required to be deployed in separate contracts. In case of ERC-721, this requires a single contract for managing a group of non-fungible tokens. However ERC-1155 works differently, it can handle any fungible and non-Fungible tokens in a single contract. This allows control of multiple tokens with different types in the same deployed contract.

As a result, the pattern avoids tons of repetitive code circulating the several contracts in the Ethereum ecosystem and saving significant storage space and gas costs.

### What is special about ERC1155?
The new standard is a powerful tool that joins fungible tokens that have been widely accepted (list of [ERC-20 tokens]) to the non-fungible tokens that are popularizing themselves (list of [NFT tokens]).

In addition, the interface ERC-1155 provides ways to make transactions more efficient. The interface defines the function “safeBatchTransferFrom” to group multiple tokens and enable atomic swaps. In other words, the interface allows multiple complex operations in a single transaction. This procedure is quite simple and does not involve complex implementation.

Backwards Compatibility is another feature of the standard. It is compatible with ERC-721 and ERC-20 which can be inherited without any issue.
ERC-1155 allows smart contracts to reference other contracts’ storage whenever it necessary. In this way, it avoids duplicating of code or misuse of storage by smart contracts. As a result, it improves the efficiency of the Ethereum ecosystem.

[ERC-20 tokens]: https://ropsten.etherscan.io/tokens
[NFT tokens]: https://nonfungible.com/
---
published: true
title: Send private transactions on private Ethereum networks
layout: post
---

`sendTransaction` and `eth_sendPrivateTransaction` are both methods for sending transactions on the Ethereum blockchain, but there are some significant differences between them.

`sendTransaction` is a method that is used to send transactions on the public Ethereum network. It is a standard method that is available in all Ethereum clients and is used to send transactions from one public account to another public account. The transaction details, such as sender address, recipient address, transaction amount, gas price, and gas limit, are publicly visible on the blockchain.

On the other hand, `eth_sendPrivateTransaction` is a method that is used to send private transactions on a **private Ethereum network**. Private networks are typically used in enterprise settings where transactions need to be kept confidential. The transaction details, including the smart contract code, are visible only to the parties involved in the transaction. This is achieved using private contracts and private transactions that are only visible to a subset of nodes on the private Ethereum network.

`eth_sendPrivateTransaction` is relevant because it provides a way for enterprises to use the Ethereum blockchain to conduct business in a private and secure manner. By keeping transactions confidential, companies can protect their proprietary information and maintain the privacy of their customers. Additionally, private Ethereum networks can provide faster transaction times and lower transaction costs than the public Ethereum network.

Private Ethereum networks are important because they allow organizations to take advantage of the benefits of blockchain technology while tailoring the network to their specific needs. By offering greater privacy, customization, control, scalability, and cost-effectiveness, private Ethereum networks are an excellent choice for businesses looking to leverage blockchain technology to achieve their strategic goals.
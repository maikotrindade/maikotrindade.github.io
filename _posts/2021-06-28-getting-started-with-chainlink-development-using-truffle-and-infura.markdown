---
published: true
title: Getting started with Chainlink development using Truffle and Infura
layout: post
---

### Chainlink
Chainlink is a decentralized network of nodes that provide data and
information from off-blockchain sources to on-blockchain smart
contracts via oracles

Chainlink greatly expands the capabilities of smart contracts by enabling access to real-world data and off-chain computation while maintaining the security and reliability guarantees inherent to blockchain technology.

This tutorial will be based on this [repo] and we will use [Truffle] – a development environment, testing framework and asset pipeline for Ethereum 

### Prerequisite
    1. Install NodeJS
    2. Install Truffle: npm install -g truffle
    3. Install Metamask
    4. Install Ganache
    5. Install VSCode
    6. Install Solidity Plugin


### Hands on: Truffle + Chainlink
`npm install --global yarn`

`mkdir Chainlink`

`cd Chainlink`

`truffle unbox smartcontractkit/box`

`yarn`

**Running tests**
Run Ganache or enable/integrate
*Kovan* testnet
`npm test`

All tests of `/test` will be executed.
There are tests about creating requests with and without Link tokens, sending these requests to oracle contract addresses, and testing contract ownership.

<img src="https://maikotrindade.com/public/img/kovan-npm-tests-chainlink.png" height="540" width="360" alt="Kovan npm tests chainlink"/>

**Note** 
You must acquire some `LINK` for interact with you smart contract. 
Get some `LINK` via [Chainlink Kovan Faucet website] 🤑 🤑 🤑 

**Ganache deployment**

`truffle migrate --network ganache --reset`

**Kovan deployment**
1. Setup Metamask and connect to Kovan network
2. Faucet: faucet.kovan.network
3. Create account and a project using Infura.io – [step-by-step tutorial]
4. Infura setup and "env.sample" file configuration

`truffle migrate --network kovan --reset`

<img src="https://maikotrindade.com/public/img/kovan-truffle-chainlink-deploy.jpeg" height="170" width="360" alt="Android great again"/>

### Helper scripts
Scripts to interact with deployed smart contract without any frontend implementation:
1. fund-contract.js

`npx truffle exec scripts/fund-contract.js --network kovan`

2. request-data.js

`npx truffle exec scripts/request-data.js --network kovan`

3. read-contract.js

`npx truffle exec scripts/read-contract.js --network kovan`

● fund-contract.js

➢ Send 1 LINK to requesting contract

● request-data.js

➢ Chainlink request to be created from the requesting contract

● read-contract.js

➢ Read the data variable of the requesting contract (current price of pair ETH/USD)

### Additional Information
[Chainlink docs]

[Chainlink official website]

[Truffle Starter kit impl]

[Code a REAL WORLD dApp with Chainlink - Ethereum, Solidity, Web3.js]

[What Is Chainlink in 5 Minutes]

[Chainlink docs]: https://docs.chain.link/docs/tutorials
[Chainlink official website]: https://chain.link
[Code a REAL WORLD dApp with Chainlink - Ethereum, Solidity, Web3.js]: https://www.youtube.com/watch?v=YLmMNocc1ys&t=1281s44-ways-to-enhance-your-smart-contract-with-chainlink/
[What Is Chainlink in 5 Minutes]: https://www.gemini.com/cryptopedia/what-is-chainlink-and-how-does-it-work
[Truffle Starter kit impl]: https://github.com/CryptoDevBR/crypto-feed-chainlink-oracle
[Truffle]: https://www.trufflesuite.com
[repo]: https://github.com/smartcontractkit/truffle-starter-kit
[step-by-step tutorial]: https://walkingtree.tech/deploying-a-smart-contract-in-rinkeby-using-infura/
[Chainlink Kovan Faucet website]: https://kovan.chain.link/
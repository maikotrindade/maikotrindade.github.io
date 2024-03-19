---
published: true
title: Nomad token - Chainlink Spring 2023 Hackathon
layout: post
---

### Introduction
No significant change happened to the $1.9 trillion travel industry. The pandemic led to unprecedented low travel volumes and financial strain, and all those business trips year-round are now 30-minute Zoom meetings.
The travel and hospitality industries (and their customers) are stuck with dated solutions, where online booking, cheap flight platforms, and lousy loyalty mechanics are not sufficing modern travelers and modern challenges and needs. Nomad rethinks the role of blockchain, empowering travelers and companies alike with unprecedented opportunities and creating a harmonious ecosystem that fosters trust, transparency, and unforgettable experiences.

### What it does
The user's journey starts when he/she decides to book a flight. To do so, the user can install the Nomad App and check the flights available. Due to the hackathon, we are using a specific flight (YYC - SEA) as a use case but the project can be more flexible and include more flight legs.

The app's home screen integrates with Nomad core (NodeJs app - Backend) which provides a list of flights based on Flights API (Aviation stack API). Our Backend is hosted on [Heroku platform] Nomad Backend.

The user can go through the sign-in flow and create an account. For this step, the Nomad app integrates with Firebase Authentication (Firebase Authentication) and lets the user choose a Google account. This step is crucial because it is part of the Seamless Web3 wallet creation - the user creates a Web3 wallet with 3 clicks and does not need to worry about the bureaucratic Web3 wallet creation. During this process, the Backend will store the user's credentials on MongoDB (MongoDB Atlas). It will automagically ether.js create the user's Ethereum wallet and store the private key on the MongoDB. We are not really concerned about security here since the wallet will not store a huge number of tokens/rewards initially.

<img src="http://maikotrindade.github.io/public/img/nomad-smartcontract.png" width="480" height="230" alt="nomad-smartcontract"/> 

The app also has two other screens: Admin and Profile. Admin screen provides triggers to the Backend force interactions with the smart contract [NomadBadge] and the Flights API for only testing purposes. The Profile gives some information about User's data on the MongoDB database and also exposes the user's private key for testing purposes.

A flight can be booked on the Home screen. The user can tap the Buy ticket button which will trigger the Backend to add a Flight (scheduled flight status) entry on the blockchain. Notice the user has to have Funds in his wallet in order to buy a flight ticket. After the flight is added on-chain, the user has an eligible flight and can get rewards from it. The Backend will update all the scheduled flight statuses and also update the smart contract.

Chainlink Automation executes the rewarding process for [NomadBadge] automatically. Once per pay, Chainlink Automation triggers the rewarding process for all the ACTIVE flights. The NomadBadge mints an NBG token if the user does not have an NBG token according to the Soulbound token specification.

We used a Soulbound token as a reference to a user’s non-transferable experience with the airline/flight. This and in conjunction with the reward system offers airlines a unique and dynamic loyalty system that engages users with their experience/status and rewards them with points they can use or transfer to others.

After that, the [NomadBadge] attributes rewards points to the user token and also transfers ERC20 tokens (NomadRewardToken - NRT) to the user's wallet. The ERC20 tokens can be transferred at any time by the user. By the end of the process, [NomadBadge] changes the flight status to REWARDED.

### Built With
- alchemyapi
- chainlink
- ethersjs
- express.js
- firebase
- heroku
- javascript
- kotlin
- mongodb
- node.js
- openzeppelin
- solidity
- typescript

[NomadBadge]: https://github.com/maikotrindade/nomad-token
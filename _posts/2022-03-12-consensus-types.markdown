---
published: true
title: "Blockchain Consensus Mechanisms Explained: PoW, PoS, BFT and More"
seo_title: "Blockchain Consensus Mechanisms: PoW, PoS, BFT and More"
layout: post
last_modified_at: 2026-11-17
tags: [Blockchain, Consensus, ProofOfWork, ProofOfStake, Ethereum, Bitcoin, BFT]
description: "How blockchain consensus works: Proof of Work, Proof of Stake, BFT, Delegated PoS, Proof of Authority and Stellar's FBA, with finality and trade-offs."
---

A consensus mechanism is how the computers in a blockchain network agree on one shared history of transactions without trusting a central authority. It decides who gets to add the next block, makes it expensive to cheat, and defines when a transaction can be considered final. This guide explains the main families (Proof of Work, Proof of Stake, BFT-style protocols, Delegated Proof of Stake, Proof of Authority and federated agreement) and the trade-offs between them.

I wrote the first version of this post in early 2022, a few months before Ethereum switched from Proof of Work to Proof of Stake. I've updated it to reflect how things work now.

## The problem consensus solves

In a decentralized network, thousands of nodes receive transactions in different orders, some nodes go offline, and some may be actively trying to cheat. For example, an attacker might try to spend the same coins twice by sending two conflicting transactions to different parts of the network.

A consensus mechanism has to answer three questions:

1. **Who proposes the next block?** Someone has to pick and order the transactions.
2. **How does everyone else agree it's valid?** Nodes check the rules and accept or reject it.
3. **When is a block final?** At what point can you be confident a transaction will never be reversed?

The second question is easy: every node checks signatures and balances itself. The first and third are where the mechanisms differ. And they all need a way to stop one person from pretending to be thousands of participants (a **Sybil attack**), usually by tying influence to something scarce.

## Proof of Work

In **Proof of Work** (PoW), the scarce resource is computing power. Miners compete to find a number that makes the block's hash fall below a target. Finding it takes enormous numbers of guesses; checking it takes one hash. The winner adds the block and collects the block reward plus fees.

Bitcoin uses PoW, with a block about every 10 minutes. If two miners find blocks at the same time, the chain temporarily splits, and nodes follow the chain with the most accumulated work. That's why PoW finality is **probabilistic**: each new block on top makes reversing a transaction much harder, and by convention six confirmations (about an hour) is treated as safe for large Bitcoin payments.

- **Strengths:** simple, battle-tested since 2009, and attacking it requires real-world hardware and electricity.
- **Weaknesses:** very high energy use, mining concentrates where electricity is cheap, and finality is never absolute.

## Proof of Stake

In **Proof of Stake** (PoS), the scarce resource is the network's own currency. Validators lock up (stake) tokens as collateral, the protocol picks validators to propose and vote on blocks, and anyone caught breaking the rules, for example by signing two conflicting blocks, loses part of their stake. That penalty is called **slashing**.

Ethereum moved to PoS in **The Merge** on September 15, 2022. According to <a href="https://ethereum.org/en/roadmap/merge/" target="_blank" rel="noopener noreferrer" title="The Merge, ethereum.org">ethereum.org</a>, it cut the network's energy use by about 99.95%. How it works today:

- A validator stakes **32 ETH** (or joins a staking pool).
- Time is divided into **slots** of 12 seconds. In each slot, one randomly chosen validator proposes a block and a committee of others votes on it (attests).
- 32 slots make an **epoch** (6.4 minutes). Once two-thirds of the staked ETH has voted in favour across two epochs, blocks are **finalized**, in about 13 minutes.

Finalized blocks can't be reverted unless validators holding at least a third of all staked ETH accept being slashed. That's called **economic finality**: reversing history is possible in theory, but it would cost billions.

- **Strengths:** a tiny fraction of PoW's energy use, explicit finality, and attackers lose their own stake.
- **Weaknesses:** influence grows with wealth, large staking providers concentrate power, and the protocol is more complex than PoW.

## BFT-style protocols

**Byzantine Fault Tolerant** (BFT) protocols come from decades of distributed-systems research. A known set of validators vote in rounds, and a block is committed once more than two-thirds of them (by count or by stake) sign it. They tolerate up to a third of validators being faulty or malicious.

CometBFT (formerly Tendermint), used by many Cosmos chains, is the best-known example. It combines BFT voting with staking to choose the validator set.

- **Strengths:** **instant finality**: once a block is committed, it's final. No waiting for confirmations.
- **Weaknesses:** every validator talks to every other one, so the validator set has to stay relatively small (usually tens to a few hundred), and the chain halts if more than a third go offline.

## Delegated Proof of Stake

In **Delegated Proof of Stake** (DPoS), token holders vote for a small number of block producers, often around 20 or so, who take turns producing blocks. EOS and TRON popularized this model.

- **Strengths:** fast blocks and high throughput, because only a few nodes need to coordinate.
- **Weaknesses:** power concentrates in a handful of producers, and voting has been criticized for vote buying and cartels.

## Proof of Authority

In **Proof of Authority** (PoA), validators are approved identities, such as known companies or institutions, and their reputation is what's at stake. There's no mining and no token staking.

PoA fits **permissioned** networks, like a consortium of banks or a company's internal chain, and some test networks. Hyperledger Besu, for example, offers BFT-style PoA protocols (QBFT and IBFT 2.0) for private Ethereum networks.

- **Strengths:** fast, cheap and predictable.
- **Weaknesses:** it's only as trustworthy as the validators, and the network isn't open to anyone.

## Federated Byzantine Agreement

**Federated Byzantine Agreement** (FBA), used by Stellar's consensus protocol (SCP), lets each node choose which other nodes it trusts (its "quorum slices"). Consensus emerges where these trust choices overlap. Unlike classic BFT, there's no single fixed validator list everyone has to agree on.

- **Strengths:** fast finality without mining or staking, and open membership.
- **Weaknesses:** safety depends on nodes choosing their quorum slices well. In practice, most nodes end up trusting the same well-known organizations.

## Side by side

| Mechanism | Sybil resistance | Finality | Example networks |
|---|---|---|---|
| Proof of Work | Computing power | Probabilistic (wait for confirmations) | Bitcoin, Litecoin |
| Proof of Stake | Staked tokens, slashing | Economic (Ethereum: about 13 minutes) | Ethereum, Cardano |
| BFT (with staking) | Staked tokens, known validator set | Instant | Cosmos chains (CometBFT) |
| Delegated PoS | Token-holder votes | Fast | EOS, TRON |
| Proof of Authority | Approved identities | Fast | Private and consortium chains |
| Federated agreement | Chosen trust relationships | Fast | Stellar |

## How to think about the trade-offs

No mechanism wins on everything. The recurring tension is between **decentralization** (how many independent parties can participate), **security** (how expensive it is to attack) and **performance** (how fast and cheap transactions are). Fewer validators make a chain faster and cheaper but easier to capture. More validators make it more robust but slower to coordinate.

When you build on a chain, the mechanism mostly shows up as one practical question: **how long do I wait before treating a transaction as done?** On Bitcoin, wait for several confirmations. On Ethereum, wait for finality for large amounts, or accept a few blocks for small ones. On a BFT chain, the first commit is final. Getting this wrong is how exchanges and bridges have lost money to chain reorganizations.

The <a href="https://ethereum.org/en/developers/docs/consensus-mechanisms/" target="_blank" rel="noopener noreferrer" title="Consensus mechanisms, ethereum.org">consensus mechanisms section on ethereum.org</a> goes deeper into PoW and PoS. If you're building on Ethereum, my <a href="https://maikotrindade.com/blockchain/solidity/2026/11/17/solidity-fundamentals-guide.html" target="_blank" rel="noopener" title="Solidity fundamentals guide">Solidity fundamentals guide</a> covers how transactions and gas work at the contract level.

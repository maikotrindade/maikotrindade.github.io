---
layout: post
title: "Ethereum Token Standards Explained: ERC-20, ERC-721, ERC-1155 and ERC-777"
seo_title: "ERC-20 vs ERC-721 vs ERC-1155 vs ERC-777 Explained"
date: 2026-11-17
published: true
categories: [blockchain, solidity]
tags: [ERC20, ERC721, ERC1155, ERC777, Ethereum, Solidity, NFT, Tokens]
description: "ERC-20, ERC-721, ERC-1155 and ERC-777 compared: fungible vs non-fungible tokens, approvals, batch transfers, receiver hooks and which standard to use."
redirect_from:
  - /2018/11/20/what-is-special-about-ERC1155.html
  - /2019/03/29/solidity-erc777-new-token-standard.html
---

A token standard is an agreed set of functions and events that a smart contract implements so wallets, exchanges and other contracts can work with it without custom code. On Ethereum, four standards cover most of what you'll meet: **ERC-20** for fungible tokens, **ERC-721** for non-fungible tokens (NFTs), **ERC-1155** for contracts that hold many token types at once, and **ERC-777**, an attempted successor to ERC-20 that's now discouraged. This guide explains what each one does, how they differ, and which to pick.

I wrote about ERC-1155 in 2018 and ERC-777 in 2019, when both were new. Some of what I wrote then didn't hold up (ERC-1155 isn't backward compatible with ERC-20, and ERC-777 turned out to be risky), so I replaced both posts with this comparison. The old URLs redirect here.

## Fungible vs non-fungible

A token is **fungible** when every unit is interchangeable. One USDC is the same as any other USDC, just like one dollar bill is as good as another. What matters is the amount.

A token is **non-fungible** when each unit is unique. A concert ticket for seat 14B isn't the same as one for seat 30F, even though both are for the same show. What matters is *which* token you own, identified by a token ID.

Some tokens sit in between: 500 copies of the same in-game sword are interchangeable with each other but different from a shield. That "semi-fungible" case is where ERC-1155 shines.

## ERC-20: fungible tokens

**ERC-20** is the original and still the most widely used standard. Stablecoins, governance tokens and wrapped ETH (WETH) are all ERC-20. Each token type lives in its own contract, which tracks a balance per address.

The interface is small:

| Function or event | Purpose |
|---|---|
| `totalSupply()` | Total tokens in existence |
| `balanceOf(account)` | Balance of an address |
| `transfer(to, amount)` | Send your own tokens |
| `approve(spender, amount)` | Allow another address to spend up to `amount` of yours |
| `allowance(owner, spender)` | How much `spender` may still spend |
| `transferFrom(from, to, amount)` | Spend tokens you were approved for |
| `Transfer`, `Approval` events | Let wallets and indexers track changes |

The `approve` + `transferFrom` pair is how contracts take payment: you approve a DEX or a lending protocol, then it pulls the tokens when you trade or deposit. It's also the biggest source of user losses, because people approve unlimited amounts to contracts that later get exploited. Two habits help: approve only what's needed, and support **EIP-2612 `permit`**, which lets users approve with an off-chain signature instead of a separate transaction.

Another gotcha: plain `transfer` to a contract that doesn't expect tokens just leaves them stuck there. Nothing in ERC-20 asks the recipient whether it can handle them.

With OpenZeppelin Contracts, a basic token takes a few lines:

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import {ERC20Permit} from "@openzeppelin/contracts/token/ERC20/extensions/ERC20Permit.sol";

contract MyToken is ERC20, ERC20Permit {
    constructor() ERC20("My Token", "MTK") ERC20Permit("My Token") {
        _mint(msg.sender, 1_000_000 * 10 ** decimals());
    }
}
```

`decimals()` defaults to 18, so balances are stored as integers scaled by 10^18. One token is `1e18` units. Forgetting this is the most common bug when an app displays balances.

## ERC-721: non-fungible tokens

**ERC-721** is the NFT standard. One contract holds a whole collection, and each token has a unique `tokenId` with exactly one owner:

- `ownerOf(tokenId)` returns the owner, and `balanceOf(owner)` counts how many tokens they hold.
- `safeTransferFrom(from, to, tokenId)` transfers a token. If the recipient is a contract, it must implement `onERC721Received`, otherwise the transfer reverts. This fixes ERC-20's stuck-tokens problem.
- `approve(to, tokenId)` approves one token, and `setApprovalForAll(operator, true)` approves an operator (like a marketplace) for the whole collection.
- The optional metadata extension adds `tokenURI(tokenId)`, which points to JSON with the name, image and attributes, usually stored on IPFS or a server.

## ERC-1155: many token types in one contract

**ERC-1155** lets one contract manage any number of token types, each identified by an `id`. Each `id` can be fungible (mint a million units), non-fungible (mint exactly one) or anything in between. It was designed for games, where one contract might hold gold coins, potions and unique legendary items.

What it changes compared with deploying one ERC-20 and one ERC-721 per asset:

- **Balances are per account and per id**: `balanceOf(account, id)`.
- **Batch operations.** `safeBatchTransferFrom` moves several token types in one transaction, and `balanceOfBatch` reads several balances in one call. That saves a lot of gas when a player trades five items at once.
- **One deployment for everything**, instead of a contract per token.
- **Mandatory receiver hooks.** Transfers to a contract call `onERC1155Received` (or the batch version), so tokens can't get stuck in contracts that don't support them.
- **Operator-only approvals.** There's `setApprovalForAll` but no per-token `approve`.
- **Metadata by template.** `uri(id)` can return one URL with an `{id}` placeholder that clients replace with the token's hex id.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {ERC1155} from "@openzeppelin/contracts/token/ERC1155/ERC1155.sol";

contract GameItems is ERC1155 {
    uint256 public constant GOLD = 0;
    uint256 public constant SWORD = 1;
    uint256 public constant CROWN = 2;

    constructor() ERC1155("https://example.com/items/{id}.json") {
        _mint(msg.sender, GOLD, 1_000_000, "");  // fungible
        _mint(msg.sender, SWORD, 500, "");       // semi-fungible
        _mint(msg.sender, CROWN, 1, "");         // unique
    }
}
```

The trade-off is compatibility. An ERC-1155 token **isn't** an ERC-20 or ERC-721 token (my 2018 post said otherwise, and that was wrong). Wallets and DeFi protocols that only speak ERC-20 can't use it directly, so a fungible ERC-1155 id won't show up in a DEX without a wrapper.

## ERC-777: the one to avoid

**ERC-777** tried to improve ERC-20 while staying backward compatible. It added **operators** (addresses allowed to send on your behalf) and **hooks**: before tokens leave an account, a `tokensToSend` function can run, and when tokens arrive, a `tokensReceived` function runs on the recipient. Hooks are registered through the ERC-1820 registry contract. The idea was to send tokens and notify a contract in a single step, without the approve-then-transfer dance.

In practice the hooks caused real damage. Because the recipient's code runs in the middle of a transfer, ERC-777 tokens opened **reentrancy** holes in contracts written with ERC-20 assumptions. In 2020, attackers used ERC-777 hooks to drain the imBTC pool on Uniswap V1 and about $25 million from the lending protocol Lendf.Me.

OpenZeppelin removed its ERC-777 implementation in Contracts 5.0. Don't use it for new tokens. If you need "transfer and call" behaviour, approve-plus-call patterns, `permit` signatures or ERC-1363 are safer options, and if you integrate with arbitrary tokens, protect your contract against reentrancy anyway.

## Which one should you use?

| You want to... | Use |
|---|---|
| Create a currency, governance or reward token | ERC-20 (add `permit`) |
| Create a collection of unique items | ERC-721 |
| Manage many item types, including unique and fungible ones, with batch transfers | ERC-1155 |
| Add hooks or "send and notify" to a fungible token | Not ERC-777. Look at ERC-1363 or a separate contract call. |

Whatever you pick, start from an audited implementation like <a href="https://docs.openzeppelin.com/contracts/" target="_blank" rel="noopener noreferrer" title="OpenZeppelin Contracts documentation">OpenZeppelin Contracts</a> rather than writing token logic yourself. The original specs are worth reading too: <a href="https://eips.ethereum.org/EIPS/eip-20" target="_blank" rel="noopener noreferrer" title="EIP-20 token standard">EIP-20</a>, <a href="https://eips.ethereum.org/EIPS/eip-721" target="_blank" rel="noopener noreferrer" title="EIP-721 non-fungible token standard">EIP-721</a> and <a href="https://eips.ethereum.org/EIPS/eip-1155" target="_blank" rel="noopener noreferrer" title="EIP-1155 multi token standard">EIP-1155</a>.

If the Solidity in the examples is new to you, start with my <a href="https://maikotrindade.com/blockchain/solidity/2026/11/17/solidity-fundamentals-guide.html" target="_blank" rel="noopener" title="Solidity fundamentals guide for 0.8.x">Solidity fundamentals guide</a>. To read token balances from a mobile app, see how to <a href="https://maikotrindade.com/2023/08/02/integrate-android-app-with-erc20-token.html" target="_blank" rel="noopener" title="Integrate an Android app with an ERC-20 token">integrate an Android app with an ERC-20 token</a>.

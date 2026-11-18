---
layout: post
title: "Solidity Fundamentals: A Practical Guide for 0.8.x"
date: 2026-11-17
published: true
categories: [blockchain, solidity]
tags: [Solidity, Ethereum, EVM, SmartContracts, Gas, Web3]
description: "Solidity 0.8.x fundamentals with compiling examples: types, data locations, mappings, events, gas, calls vs transactions, globals and inheritance."
image: /public/img/evm.png
redirect_from:
  - /2017/11/07/solidity-basics.html
  - /2017/12/11/solidity-hash-type-casting.html
  - /2018/01/15/solidity-block-transaction-properties.html
  - /2018/01/24/solidity-difference-gas-gas-price-fee.html
  - /2018/02/20/solidity-call-vs-transaction.html
  - /2020/04/11/the-ethereum-virtual-machine.html
  - /2020/05/01/structure-of-smart-contract.html
  - /2020/07/14/basic-of-solidity-mappings.html
  - /2020/09/29/inheritance-in-solidity-explained.html
---

Solidity is the main language for writing smart contracts on Ethereum and other EVM chains. This guide covers the fundamentals you need for Solidity 0.8.x: how a contract is laid out, value and reference types, data locations, mappings, events and errors, how gas is charged, the difference between a call and a transaction, the global variables you'll reach for, and how inheritance works. Every example compiles with the 0.8 compiler.

Between 2017 and 2020 I wrote nine short posts on these topics. A lot changed since then: `now` and `msg.gas` are gone, arithmetic overflow reverts by default, Ethereum moved to proof of stake, and fees work differently after EIP-1559. So I merged them into this one guide and brought everything up to date. The old URLs redirect here.

## How the EVM runs your code

Solidity doesn't run directly. The compiler (`solc`) turns it into **bytecode**, a list of low-level instructions (opcodes) for the **Ethereum Virtual Machine**. Every Ethereum node runs the same EVM, which is why every node reaches the same result for the same transaction. Clients implement it in several languages: Geth in Go, Nethermind in C#, Besu in Java and Reth in Rust, among others.

<img src="https://maikotrindade.com/public/img/evm.png" width="340" height="160" alt="Diagram of the Ethereum Virtual Machine executing smart contract bytecode"/>

A few properties of the EVM explain a lot of Solidity's design:

- It's a **stack machine** with 256-bit words. That's why `uint256` is the "natural" integer size, and why smaller types don't always save gas.
- Each opcode has a fixed **gas** cost. Writing to storage is by far the most expensive thing you can do.
- A contract has several places to keep data: **storage** (persistent, on chain), **memory** (temporary, wiped after the call), **calldata** (the read-only input of the call) and the stack. Since the Cancun upgrade there's also **transient storage**, which lives only for the duration of a transaction.

The <a href="https://ethereum.org/en/developers/docs/evm/" target="_blank" rel="noopener noreferrer" title="Ethereum Virtual Machine documentation on ethereum.org">EVM page on ethereum.org</a> goes deeper if you're curious about opcodes and the execution model.

## Anatomy of a contract

A contract is a bit like a class: it groups state, functions and types. Here's a small but complete one. I'll refer back to it in the rest of the guide.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

contract TipJar {
    // State variables live in storage
    address public immutable owner;
    uint256 public constant MIN_TIP = 0.001 ether;

    struct Tip {
        address from;
        uint256 amount;
        string message;
    }

    Tip[] private tips;
    mapping(address tipper => uint256 total) public totalByTipper;

    event TipReceived(address indexed from, uint256 amount, string message);
    error TipTooSmall(uint256 sent, uint256 minimum);
    error NotOwner();
    error WithdrawFailed();

    modifier onlyOwner() {
        if (msg.sender != owner) revert NotOwner();
        _;
    }

    constructor() {
        owner = msg.sender;
    }

    function tip(string calldata message) external payable {
        if (msg.value < MIN_TIP) revert TipTooSmall(msg.value, MIN_TIP);
        tips.push(Tip(msg.sender, msg.value, message));
        totalByTipper[msg.sender] += msg.value;
        emit TipReceived(msg.sender, msg.value, message);
    }

    function tipCount() external view returns (uint256) {
        return tips.length;
    }

    function withdraw() external onlyOwner {
        (bool ok, ) = payable(owner).call{value: address(this).balance}("");
        if (!ok) revert WithdrawFailed();
    }
}
```

The parts, from top to bottom:

- **SPDX license line and `pragma`**: the license is metadata, and `pragma solidity ^0.8.24` means "any 0.8 compiler from 0.8.24 up".
- **State variables**: `owner`, `tips` and `totalByTipper` are stored on chain. `constant` values are inlined at compile time and `immutable` values are set once in the constructor. Neither one uses a storage slot, so reading them is cheap.
- **Struct**: `Tip` groups related fields into a custom type.
- **Mapping**: `totalByTipper` is a key-value store (more on mappings below).
- **Event and errors**: `TipReceived` is for off-chain listeners, and the custom errors describe why a call reverted.
- **Modifier**: `onlyOwner` wraps a function with a check. The `_;` marks where the function body runs.
- **Constructor**: runs once, at deployment.
- **Functions**: `tip` accepts Ether because it's `payable`, `tipCount` only reads state because it's `view`, and `withdraw` sends Ether out.

## Types

Solidity is statically typed, so every variable's type is known at compile time.

### Value types

| Type | What it holds |
|---|---|
| `bool` | `true` or `false` |
| `uint8` … `uint256` | Unsigned integers in steps of 8 bits. `uint` is an alias for `uint256`. |
| `int8` … `int256` | Signed integers. `int` is an alias for `int256`. |
| `address` | A 20-byte Ethereum address |
| `address payable` | An address you can send Ether to |
| `bytes1` … `bytes32` | Fixed-size byte arrays |
| `enum` | A user-defined set of named constants |

Two things changed in 0.8 that matter every day:

- **Arithmetic is checked.** Overflow and underflow revert instead of silently wrapping around. That's why you rarely see SafeMath in new code. When you're sure a value can't overflow and you want to save gas, wrap it in an `unchecked { ... }` block.
- **`**` is the power operator.** `2 ** 8` is 256. `^` is bitwise XOR, which is an easy mistake if you come from other languages (my 2017 post got this wrong).

### Reference types

`string`, `bytes` (a dynamic byte array), arrays (`uint256[]`, `address[10]`), structs and mappings are **reference types**. For these you have to say where the data lives, which brings us to data locations.

## Data locations: storage, memory and calldata

Every reference-type variable has a location:

- **`storage`**: persistent contract state. State variables are always in storage.
- **`memory`**: a temporary copy that disappears when the function returns.
- **`calldata`**: the read-only input of an external call. It's the cheapest option for parameters you don't modify.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

contract Locations {
    uint256[] public numbers;

    function addAll(uint256[] calldata input) external {
        for (uint256 i = 0; i < input.length; i++) {
            numbers.push(input[i]);
        }
    }

    function doubled() external view returns (uint256[] memory result) {
        result = new uint256[](numbers.length);
        for (uint256 i = 0; i < numbers.length; i++) {
            result[i] = numbers[i] * 2;
        }
    }

    function resetFirst() external {
        uint256[] storage ref = numbers; // a pointer to storage, not a copy
        ref[0] = 0;
    }
}
```

The behavior that trips people up: assigning storage to a `memory` variable **copies** the data, so changes to the copy don't touch the contract state. Assigning it to a `storage` variable creates a **reference**, so changes do. Since 0.5.0 you must write the location explicitly for reference-type parameters and local variables, so the compiler won't let you guess. (Older tutorials, including mine, say local variables default to storage. That hasn't been true for years.)

## Mappings

A mapping is Solidity's hash table:

```solidity
mapping(address user => uint256 balance) public balances;
mapping(address owner => mapping(address spender => uint256 amount)) public allowance;
```

The named keys and values (`user`, `balance`) are optional and were added in 0.8.18. They make code and generated getters easier to read.

Mappings behave differently from a dictionary in most languages:

- **Every key exists.** A key that was never set returns the type's zero value (`0`, `false`, `address(0)`). You can't tell "set to zero" apart from "never set" without tracking it yourself.
- **No length and no iteration.** The keys aren't stored, only the hashed slots. If you need to list entries, keep a separate array of keys alongside the mapping.
- **Storage only.** You can't create a mapping in memory or pass one to an external function.
- **Nesting works**, as the ERC-20 `allowance` above shows.
- A `public` mapping gets an automatic getter that takes the key as an argument.

Looping over large arrays costs gas on every iteration and can hit the block gas limit. So the usual pattern is: write to a mapping for lookups, emit an event for history, and let off-chain code (an indexer, or your app) build lists from those events.

## Events and custom errors

**Events** write data to the transaction's logs. They're cheap compared to storage, and apps and indexers can subscribe to them. Contracts can't read logs, so events are only for the outside world.

```solidity
event Transfer(address indexed from, address indexed to, uint256 value);
emit Transfer(msg.sender, to, amount);
```

Up to three parameters can be `indexed`, which makes them filterable (for example, "all transfers to this address").

**Custom errors**, added in 0.8.4, are the modern way to revert:

```solidity
error InsufficientBalance(uint256 available, uint256 required);

if (balance < amount) revert InsufficientBalance(balance, amount);
```

They're cheaper than `require(condition, "long message")` because the error is encoded as a 4-byte selector plus its arguments instead of a string. Your app can also decode them and show a meaningful message. You'll still see `require` a lot, and since 0.8.26 it also accepts a custom error as its second argument.

## Functions: visibility and state mutability

### Visibility

| Visibility | Who can call it |
|---|---|
| `external` | Only from outside (other contracts, transactions). Inside the contract you'd need `this.f()`. |
| `public` | From anywhere. For state variables, the compiler generates a getter. |
| `internal` | This contract and contracts that inherit from it. This is the default for state variables. |
| `private` | Only this contract. Not even derived contracts. |

`private` doesn't mean secret. Everything in storage is readable by anyone running a node, so never put passwords or keys in a contract.

### State mutability

- **`view`**: reads state but doesn't change it.
- **`pure`**: neither reads nor changes state (calculations, encoding).
- **`payable`**: can receive Ether with the call. Functions without it revert if Ether is sent.
- No keyword means the function can change state.

## Calls vs transactions

There are two ways to run a contract function from outside the chain, and they're very different.

A **call** (`eth_call` in JSON-RPC) runs the function on the node you're connected to and returns the result right away. Nothing is signed, nothing is broadcast and nothing is saved, so it costs you nothing. You use it to read data, for example `tipCount()`.

A **transaction** is signed by an account, broadcast to the network, included in a block by a validator and executed by every node. It can change state, it costs gas, and you don't get the function's return value back directly. You read the outcome from the receipt and its events. You use it for anything that writes, like `tip()`.

Inside the EVM, when one contract calls another, that's a **message call**. It runs as part of the same transaction and shares its gas.

One nuance: a `view` function is only free when you call it off chain. If a transaction calls it as part of other work, its execution costs gas like any other code.

## Gas, gas price and fees

**Gas** measures how much computation and storage a transaction uses. It's a unit of work, not a currency. You pay for it in ETH.

Since the London upgrade (EIP-1559, in 2021), the fee works like this:

```
fee = gas used × (base fee + priority fee)
```

- The **base fee** is set by the protocol and goes up or down with network demand. It's **burned**, not paid to anyone.
- The **priority fee** (the "tip") goes to the validator who includes your transaction.
- You also set a **gas limit** (the most gas you'll allow) and a **max fee per gas** (the most you'll pay per unit). If the base fee spikes above your max fee, the transaction just waits.

If a transaction reverts, its state changes are undone, but it still lands in a block and you still pay for the gas used up to that point. If it runs **out of gas**, you pay for the whole gas limit.

### Writing cheaper contracts

The habits that make the biggest difference:

- **Touch storage as little as possible.** Writing a new non-zero value to a storage slot costs about 20,000 gas, while memory operations cost a handful. Read a storage value once into a local variable if you use it several times.
- **Use `constant` and `immutable`** for values that don't change.
- **Pack small variables.** Storage is organized in 32-byte slots, and variables declared next to each other share a slot if they fit (for example `uint128 a; uint64 b; uint64 c;`).
- **Use `calldata`** for external function parameters you only read.
- **Use custom errors** instead of long revert strings.
- **Keep contracts under the 24 KB size limit** (EIP-170) by splitting logic or using libraries.

## Global variables

These are always available. I've noted the ones that changed since older tutorials.

| Variable | Meaning |
|---|---|
| `msg.sender` | The address that made the current call |
| `msg.value` | Wei sent with the call |
| `msg.data` | The complete calldata |
| `msg.sig` | The first 4 bytes of the calldata (the function selector) |
| `block.number` | The current block number |
| `block.timestamp` | The block timestamp in seconds. Replaces `now`, which was removed in 0.7.0. |
| `block.chainid` | The chain ID (1 for Ethereum mainnet) |
| `block.basefee` | The current base fee (since EIP-1559) |
| `block.prevrandao` | Randomness from the beacon chain. Replaces `block.difficulty`, which no longer means anything after the move to proof of stake. |
| `block.coinbase` | The address of the block's fee recipient |
| `block.gaslimit` | The block's gas limit |
| `blockhash(n)` | The hash of one of the 256 most recent blocks. It used to be `block.blockhash`. |
| `gasleft()` | Remaining gas. Replaces `msg.gas`, which was removed in 0.5.0. |
| `tx.origin` | The account that started the transaction |
| `tx.gasprice` | The gas price of the transaction |

Two warnings. **Don't use `tx.origin` for authorization.** If your contract checks `tx.origin == owner`, a malicious contract the owner interacts with can call yours and pass the check. Use `msg.sender`. And **don't treat `block.timestamp` or `block.prevrandao` as a secure source of randomness** for anything valuable. Validators have some influence over both. Use a verifiable randomness service such as Chainlink VRF. Oracles like Chainlink are also how a contract gets any off-chain data; I used them in my <a href="https://maikotrindade.com/2023/06/28/nomad-token-chainlink-hackathon.html" target="_blank" rel="noopener" title="Nomad Token, a Chainlink hackathon project">Nomad Token hackathon project</a>.

## Hashing and type conversion

### keccak256

`keccak256` takes a single `bytes` argument and returns a `bytes32` hash. To hash several values, encode them first:

```solidity
bytes32 id = keccak256(abi.encode(user, nonce));
```

`abi.encodePacked` gives a shorter encoding, but with two or more dynamic types (like two strings) different inputs can produce the same bytes: `("ab", "c")` and `("a", "bc")` collide. Prefer `abi.encode` unless you know why you need packed encoding.

### Converting between types

**Implicit** conversions happen only when no information can be lost. A `uint8` fits in a `uint256`, so this compiles:

```solidity
uint8 small = 8;
uint256 big = small;
```

Going the other way needs an **explicit** conversion, and it silently cuts off the higher-order bits:

```solidity
uint32 a = 0x12345678;
uint16 b = uint16(a); // 0x5678
```

Since 0.8.0, an explicit conversion can change only one thing at a time: sign, size or kind of type. `uint16(int8(x))` doesn't compile because it changes both sign and size. You have to go through an intermediate type, for example `uint16(uint8(x))`, which makes the risk visible in the code.

Address conversions follow the same idea: `address(uint160(value))` turns a number into an address, and `payable(addr)` turns an `address` into an `address payable`.

## Inheritance

A contract inherits from others with `is`. When you deploy it, the compiler copies the code from every parent into **one contract with one address**. Calls to parent functions are just internal jumps.

A function must be marked `virtual` to be overridable, and the overriding function must say `override`:

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

contract Grandparent {
    function who() public pure virtual returns (string memory) {
        return "Grandparent";
    }
}

contract Parent is Grandparent {
    function who() public pure virtual override returns (string memory) {
        return "Parent";
    }
}

contract Uncle is Grandparent {
    function who() public pure virtual override returns (string memory) {
        return "Uncle";
    }
}

contract Child is Parent, Uncle {
    function who() public pure override(Parent, Uncle) returns (string memory) {
        return super.who(); // "Uncle"
    }
}
```

With multiple inheritance, order matters. List parents from "most base-like" to "most derived". Solidity linearizes the hierarchy (using C3 linearization, like Python), and `super` calls the next contract in that order, not necessarily the parent you expect. For `Child is Parent, Uncle`, the order from most derived is `Child`, `Uncle`, `Parent`, `Grandparent`, so `super.who()` returns `"Uncle"`. When a function exists in more than one parent, you have to list them all in `override(Parent, Uncle)`.

A few more rules:

- A child can use everything that isn't `private`: `internal` and `public` state and functions.
- An **abstract contract** has at least one function without an implementation and can't be deployed on its own.
- An **interface** only declares external functions. It's what you use to call another contract when you don't have its source code, for example `IERC20(token).transfer(to, amount)`.

In practice you'll mostly inherit from audited libraries like <a href="https://docs.openzeppelin.com/contracts/" target="_blank" rel="noopener noreferrer" title="OpenZeppelin Contracts documentation">OpenZeppelin Contracts</a> instead of writing token logic or access control yourself.

## Where to go next

To try any of these examples, paste them into <a href="https://remix.ethereum.org" target="_blank" rel="noopener noreferrer" title="Remix, the browser-based Solidity IDE">Remix</a>, which runs in the browser. For real projects, use <a href="https://getfoundry.sh" target="_blank" rel="noopener noreferrer" title="Foundry, a Solidity development toolkit">Foundry</a> or <a href="https://hardhat.org" target="_blank" rel="noopener noreferrer" title="Hardhat, an Ethereum development environment">Hardhat</a>. Truffle, which my older posts used, was retired in 2023.

The <a href="https://docs.soliditylang.org/en/latest/" target="_blank" rel="noopener noreferrer" title="Official Solidity documentation">official Solidity documentation</a> is the reference for everything here, and its list of breaking changes per version explains why older code doesn't compile anymore. If you build on Android, I also wrote about how to <a href="https://maikotrindade.com/2023/08/02/integrate-android-app-with-erc20-token.html" target="_blank" rel="noopener" title="Integrate an Android app with an ERC-20 smart contract">integrate an Android app with an ERC-20 smart contract</a>.

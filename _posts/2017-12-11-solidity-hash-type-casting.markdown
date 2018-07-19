---
published: true
title: Solidity – Hashes and Typecasting
layout: post
---


### Hashes
In [Solidity], it is possible to use the keccak256 function to get a hash. Ethereum’s KECCAK-256 algorithm produces a 256-bit hexadecimal number. 

> keccak256(...) returns (bytes32):
> compute the Ethereum-SHA-3 (Keccak-256) hash of the (tightly packed) arguments

Usage Examples
```javascript
keccak256(6382179)
keccak256(97, 98, 99)
```

### Typecasting
[Solidity] is a statically typed language, which means that the type of each variable (state and local) needs to be specified at compile-time. 
Solidity is able to perform operations between two variables that have the same type. Therefore you can convert one of the variables to the type of the others. 

```javascript
uint256 z = y * uint256(x);
uint8 x = 8;
uint256 y = 10 ** 18;
```

[Solidity]: http://solidity.readthedocs.io/en/v0.4.24/
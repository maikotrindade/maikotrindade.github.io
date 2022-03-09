---
published: true
title: Basic of Mappings in Solidity
layout: post
---


Mappings are one of the most used complex data types in Solidity. Mappings act as hash tables which consist of key types and corresponding value type pairs – pretty similar to hash tables or dictionaries in other languages. They help in storing key-value pairs and enable retrieving values based on the supplied key.


Mappings are declared using the `mapping` keyword followed by data types for both key and value separated by the `=>` notation. Mappings have identifiers like any other data type and they can be used to access the mapping and can only have type of storage and are generally used for state variables. Solidity automatically creates a getter function for it.
 
Although it is similar to a hash table and dictionary, Solidity does not allow iterating through mapping. A value from mapping can be retrieved if the key is known. The next example illustrates working with mapping.


Another characteristic about mapping is the absence of iteration support but there are ways to work round this limitation. Notice that iterating and looping are an expensive operation in Ethereum in terms of gas usage and should generally be avoided.


### 💡 Gotchas 

* Mappings do not have a length, nor do they have a concept of a key or a value being set
* It is also possible to have nested mapping, that is mapping consisting of mappings
* Mappings can only be used for state variables that act as storage reference types
* Mapping cannot be declared within functions as memory mappings
* When mappings are initialized every possible key exists in the mappings and are mapped to values whose byte-representations are all zeros


### Additional Information
	
[Types in Solidity] – Solidity Docs v0.4.21

[Types in Solidity]: https://docs.soliditylang.org/en/v0.4.21/types.html



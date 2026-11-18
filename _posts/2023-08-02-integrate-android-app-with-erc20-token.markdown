---
published: true
title: "Integrate an Android App with an ERC-20 Token in Kotlin"
layout: post
last_modified_at: 2026-11-17
tags: [Android, Kotlin, ERC20, Ethereum, JSONRPC, Web3, Coroutines]
description: "Read ERC-20 token balances in an Android app with Kotlin: JSON-RPC eth_call, ABI encoding, decimals, RPC keys and why writes belong in a wallet."
---

An Android app can read data from an ERC-20 token, like a user's balance, without any blockchain SDK: it sends a JSON-RPC `eth_call` to an Ethereum node and decodes the result. Sending tokens is a different problem, because it needs a signed transaction and a private key that your app shouldn't hold. This guide shows how to read a balance in Kotlin, how the ABI encoding works under the hood, and how to handle writes safely.

The first version of this post, from 2023, wasn't really about Android. It described a Node.js GraphQL server and called a `web3.eth.getToken` method that doesn't exist in web3.js. I rewrote it around what an Android developer actually needs.

## How an app talks to Ethereum

Your app never connects to "the blockchain" directly. It talks to an **Ethereum node** over **JSON-RPC**, a simple protocol where you POST a JSON request and get JSON back. Most apps use a hosted node provider such as Infura, Alchemy or QuickNode rather than running their own.

For reading data, the method you need is **`eth_call`**. It runs a contract function on the node without creating a transaction, so it's free and returns immediately. (My <a href="https://maikotrindade.com/blockchain/solidity/2026/11/17/solidity-fundamentals-guide.html" target="_blank" rel="noopener" title="Solidity fundamentals guide">Solidity fundamentals guide</a> explains the difference between calls and transactions in more detail.)

## Encoding the call

Contracts don't receive function names. They receive **calldata**: a 4-byte **function selector** followed by the arguments, each padded to 32 bytes. The selector is the first 4 bytes of the keccak-256 hash of the function signature.

For the ERC-20 functions you'll use most:

| Function | Selector |
|---|---|
| `balanceOf(address)` | `0x70a08231` |
| `decimals()` | `0x313ce567` |
| `symbol()` | `0x95d89b41` |
| `transfer(address,uint256)` | `0xa9059cbb` |

So `balanceOf(0xAbC…123)` becomes `0x70a08231` followed by the address without its `0x`, left-padded with zeros to 64 hex characters. The node returns the balance as a 32-byte hex number.

## Reading a balance in Kotlin

Here's a small client using OkHttp and coroutines. It doesn't need any web3 library:

```kotlin
class Erc20Reader(
    private val rpcUrl: String,
    private val http: OkHttpClient = OkHttpClient()
) {
    suspend fun balanceOf(token: String, owner: String): BigInteger {
        val data = "0x70a08231" + owner.removePrefix("0x").lowercase().padStart(64, '0')
        return ethCall(token, data).toBigInteger()
    }

    suspend fun decimals(token: String): Int =
        ethCall(token, "0x313ce567").toBigInteger().toInt()

    private suspend fun ethCall(to: String, data: String): String = withContext(Dispatchers.IO) {
        val payload = JSONObject()
            .put("jsonrpc", "2.0")
            .put("id", 1)
            .put("method", "eth_call")
            .put("params", JSONArray()
                .put(JSONObject().put("to", to).put("data", data))
                .put("latest"))

        val request = Request.Builder()
            .url(rpcUrl)
            .post(payload.toString().toRequestBody("application/json".toMediaType()))
            .build()

        http.newCall(request).execute().use { response ->
            if (!response.isSuccessful) throw IOException("HTTP ${response.code}")
            val json = JSONObject(response.body?.string() ?: throw IOException("Empty body"))
            json.optJSONObject("error")?.let { throw IOException(it.optString("message")) }
            json.getString("result")
        }
    }

    private fun String.toBigInteger(): BigInteger =
        BigInteger(removePrefix("0x").ifEmpty { "0" }, 16)
}
```

A few details worth pointing out:

- The network call runs on `Dispatchers.IO`, so `balanceOf` is safe to call from a `ViewModel` on the main thread.
- JSON-RPC errors come back with HTTP 200 and an `error` object, so checking the status code isn't enough.
- Balances can exceed `Long`, so use `BigInteger`. A token with 18 decimals and a few million units already overflows a `Long`.

## Turning units into a readable amount

ERC-20 balances are integers. A token with 18 decimals stores 1.5 tokens as `1500000000000000000`. Convert with `BigDecimal` before showing anything to the user, never with `Double`:

```kotlin
fun formatTokenAmount(raw: BigInteger, decimals: Int): String =
    BigDecimal(raw)
        .movePointLeft(decimals)
        .setScale(minOf(decimals, 4), RoundingMode.DOWN)
        .stripTrailingZeros()
        .toPlainString()
```

`formatTokenAmount(BigInteger("1500000000000000000"), 18)` returns `"1.5"`. Round **down** for balances, so you never show a user more than they can actually send. And always read `decimals()` from the contract: USDC and USDT use 6, most other tokens use 18.

## Using it from a ViewModel

```kotlin
class WalletViewModel(private val reader: Erc20Reader) : ViewModel() {
    private val _balance = MutableStateFlow<String?>(null)
    val balance: StateFlow<String?> = _balance.asStateFlow()

    fun refresh(token: String, owner: String) {
        viewModelScope.launch {
            _balance.value = try {
                val raw = reader.balanceOf(token, owner)
                formatTokenAmount(raw, reader.decimals(token))
            } catch (e: IOException) {
                null
            }
        }
    }
}
```

`decimals()` never changes for a given token, so in a real app you'd cache it instead of fetching it on every refresh. For live updates, either poll on an interval while the screen is visible or subscribe to the token's `Transfer` events through a WebSocket provider.

## Don't ship your RPC key

Hosted node URLs usually contain an API key, like `https://mainnet.infura.io/v3/YOUR_KEY`. Anything inside an APK can be extracted, so a key in `BuildConfig` is effectively public. Someone can copy it and burn through your quota.

Options, from simplest to most robust:

- Restrict the key in the provider's dashboard: most providers let you allowlist contract addresses and JSON-RPC methods and set rate limits.
- Put a small backend in front of the node that forwards only the calls your app needs.
- Use a public RPC endpoint for low-volume reads, accepting lower reliability.

## Writing: let a wallet sign

Reading is free and needs no keys. **Transferring tokens** means sending a transaction to `transfer(address,uint256)`, which must be signed with the user's private key and pay gas.

Don't generate or store users' private keys in your app unless building a wallet is your product. Key storage, backup and recovery are hard, and a bug can lose people's money for good. The usual approaches:

- **Connect to the user's wallet** with WalletConnect (now Reown). Your app builds the transaction, the wallet app shows it to the user and signs it, and you get back the transaction hash.
- **Do it on a backend**, when the app's operator is the one sending tokens, for example rewards. The backend holds its own key in a secrets manager and the app just calls an API.

My <a href="https://maikotrindade.com/2023/06/28/nomad-token-chainlink-hackathon.html" target="_blank" rel="noopener" title="Nomad Token Chainlink hackathon project">Nomad Token hackathon project</a> used the second approach: the Android app called a Node.js backend that used ethers.js to talk to the contracts, and the contracts sent ERC-20 reward tokens to users' wallets.

## Where to go from here

Hand-encoding calls is fine for a few read-only functions and helps you understand what's going on. Once you need many contract functions, events or transaction signing, use a library: <a href="https://docs.web3j.io/" target="_blank" rel="noopener noreferrer" title="web3j documentation">web3j</a> can generate type-safe Kotlin or Java wrappers from a contract's ABI.

For how ERC-20 compares with NFT standards like ERC-721 and ERC-1155, see my <a href="https://maikotrindade.com/blockchain/solidity/2026/11/17/ethereum-token-standards-erc20-erc721-erc1155.html" target="_blank" rel="noopener" title="Ethereum token standards explained">guide to Ethereum token standards</a>. The <a href="https://ethereum.org/en/developers/docs/apis/json-rpc/" target="_blank" rel="noopener noreferrer" title="Ethereum JSON-RPC API reference">JSON-RPC reference on ethereum.org</a> lists every method a node supports.

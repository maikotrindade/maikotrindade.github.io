---
published: true
title: Coroutines basics 
layout: post
---

### Intro

Kotlin, as a language, provides only minimal low-level APIs in its standard library to enable various other libraries to utilize [coroutines]. Unlike many other languages with similar capabilities, *async* and *await* are not keywords in Kotlin and are not even part of its standard library. Moreover, Kotlin's concept of suspending function provides a safer and less error-prone abstraction for asynchronous operations than futures and promises.

On Android, coroutines help to solve two primary problems:
	
* Manage long-running tasks that might otherwise block the main thread and cause your app to freeze.
* Providing main-safety, or safely calling network or disk operations from the main thread.

### Get Started 

Essentially, coroutines are light-weight threads. They are launched with launch coroutine builder in a context of some `CoroutineScope`. Here we are launching a new coroutine in the `GlobalScope`, meaning that the lifetime of the new coroutine is limited only by the lifetime of the whole application.

See this example: 

>	import kotlinx.coroutines.*
>	
>	fun main() {
>	    GlobalScope.launch { // launch a new coroutine
>		delay(1000L) // non-blocking delay
>		println("World!")
>	}
>	
>		println("Hello,") // main thread continues
>		Thread.sleep(2000L) // block main thread
>	}
 
Coroutines allows us to mix _blocking_ and _non-blocking_ code in the same place. See the following example which has two delays. The first one is a _non-blocking_ code inside a courotine and the second is _blocking_. Both work correctly once they are wrapped bt another courotine.

*Note*: Delaying for a time while another coroutine is working is not a good approach.

>	import kotlinx.coroutines.*
>	
>	fun main() = runBlocking<Unit> { // start main coroutine
>		GlobalScope.launch { // launch a new coroutine
>		delay(1000L)
>		println("World!")
>	}
>	    
>		println("Hello,") // main coroutine continues
>		delay(2000L)      // delaying
>	}

### Designate a CoroutineScope

When defining a coroutine, you must also designate its `coroutineScope`. A `coroutineScope` manages one or more related coroutines. You can also use a `coroutineScope` to start a new coroutine within that scope. Unlike a dispatcher, however, a `coroutineScope` doesn't run the coroutines.

One important function of `coroutineScope` is stopping coroutine execution when a user leaves a content area within your app. Using `coroutineScope`, you can ensure that any running operations stop correctly.

`runBlocking` and `coroutineScope` may look similar because they both wait for its body and all its children to complete. The main difference between these two is that the `runBlocking` method blocks the current thread for waiting, while `coroutineScope` just suspends, releasing the underlying thread for other usages. Because of that difference, `runBlocking` is a regular function and `coroutineScope` is a suspending function.

[coroutines]: https://github.com/Kotlin/kotlinx.coroutines
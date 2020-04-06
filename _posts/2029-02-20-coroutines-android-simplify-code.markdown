---
published: true
title: Simplify your Android code with Coroutines
layout: post
---

 Kotlin Coroutines in an Android app—a new way of managing background threads that can simplify code by reducing the need for callbacks. Coroutines are a Kotlin feature that converts async callbacks into sequential code. Code written sequentially is typically easier to read, and can even use language features such as exceptions.

 In the end, they do the exact same thing: wait until a result is available from a long-running task and continue execution. However, in code they look very different.

 The keyword `suspend` is Kotlin's way of marking a function, or function type, available to coroutines. When a coroutine calls a function marked `suspend`, instead of blocking until that function returns like a normal function call, it suspends execution until the result is ready then it resumes where it left off with the result. While it's suspended waiting for a result, it unblocks the thread that it's running on so other functions or coroutines can run.

*Note*
>	The pattern of async and await in other languages is based on coroutines. If you're familiar with this pattern, the suspend keyword is similar to async. However in Kotlin, await() is implicit when calling a suspend function.

### Scopes

All coroutines run inside a CoroutineScope. A scope controls the lifetime of coroutines through its job. When you cancel the job of a scope, it cancels all coroutines started in that scope. On Android, you can use a scope to cancel all running coroutines when, for example, the user navigates away from an Activity. Scopes also allow you to specify a default dispatcher. A dispatcher controls which thread runs a coroutine.
	
*GlobalScope* - Lifetime of the new coroutine is limited only by the lifetime of the whole application

*CoroutineScope* - Is destroyed after all launched children are completed
	
*MainScope* - Scope for UI applications and uses Dispatchers.Main


*Note*
>	Libraries like Room and Retrofit offer main-safety out of the box when using coroutines, so you don't need to manage threads to make network or database calls. This can often lead to substantially simpler code.

### Channels

`Channels`  are a way to communicate (transfer data) between coroutines similar to a blocking queue.
It Uses `send` and `receive` for normal values, produce and consume for streams. Moreover, `Channels` can be closed to indicate no more elements are coming.


### Exception handling
Coroutines will delegate uncaught exceptions to the system's uncaught exception handler. On Android, the handler will output the exception and crash the app.

```
try {
    GlobalScope.launch {
        throw NullPointerException()
    }
} catch (e: Exception) {
    // Exceptions will never land here because `launch` propagates uncaught exceptions
    // to the default handler and will never pass them to the outer scope.
    System.err.println("Caught exception! $e")
}
```
 
### Additional Information
	
[Use Kotlin Coroutines in your Android App] by Google

[Android Kotlin Fundamentals 06.2: Coroutines and Room] by Google

[Understand Kotlin Coroutines on Android] at Google/IO 19


[Use Kotlin Coroutines in your Android App]: https://codelabs.developers.google.com/codelabs/kotlin-coroutines/#0
[Android Kotlin Fundamentals 06.2: Coroutines and Room]: https://codelabs.developers.google.com/codelabs/kotlin-android-training-coroutines-and-room/#0
[Understand Kotlin Coroutines on Android]: https://www.youtube.com/watch?v=BOHK_w09pVA


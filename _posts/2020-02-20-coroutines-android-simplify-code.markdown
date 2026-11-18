---
published: true
title: "Kotlin Coroutines on Android: A Practical Guide"
layout: post
last_modified_at: 2026-11-17
tags: [Kotlin, Coroutines, Android, StructuredConcurrency, Flow]
description: "Kotlin coroutines on Android: suspend functions, scopes, dispatchers, structured concurrency, cancellation, exceptions and testing with runTest."
redirect_from:
  - /2019/12/05/coroutines-basics.html
---

Kotlin coroutines let you write asynchronous code that reads like ordinary sequential code. On Android they solve two problems: keeping long-running work off the main thread so the UI doesn't freeze, and cancelling that work automatically when the screen that started it goes away. This guide covers what you need day to day: suspend functions, scopes, dispatchers, structured concurrency, cancellation, exceptions and testing.

I first wrote about coroutines in 2019 and 2020, when `GlobalScope` examples were everywhere. Those examples aged badly, so I merged both posts into this one and rewrote it around the patterns Android uses now.

## Suspend functions

A `suspend` function can pause without blocking the thread it runs on. While it waits (for a network response, a database query, a delay), the thread is free to do other work. When the result is ready, the function resumes where it left off.

```kotlin
suspend fun loadProfile(id: String): Profile {
    val user = api.fetchUser(id)          // suspends, doesn't block
    val posts = api.fetchPosts(user.id)   // runs after the first call returns
    return Profile(user, posts)
}
```

Compare that with callbacks: no nesting, and you can use `try`/`catch`, loops and `return` the way you normally would. If you know `async`/`await` from JavaScript or C#, a call to a suspend function is like an implicit `await`.

You can only call a suspend function from another suspend function or from a coroutine. That restriction is the point: it forces every piece of async work to belong to some coroutine, which belongs to some scope.

## Scopes: who owns the work

A **coroutine scope** defines how long its coroutines may live. Cancel the scope and everything started in it is cancelled. On Android you rarely create scopes yourself, because the lifecycle libraries give you the right ones:

- **`viewModelScope`**: cancelled when the `ViewModel` is cleared. Use it for work that should survive rotation but not leaving the screen.
- **`lifecycleScope`**: cancelled when the `Activity` or `Fragment` is destroyed.
- **`rememberCoroutineScope()`** and **`LaunchedEffect`** in Compose: tied to the composable's place in the UI.

```kotlin
class ProfileViewModel(private val repository: ProfileRepository) : ViewModel() {
    private val _state = MutableStateFlow<ProfileState>(ProfileState.Loading)
    val state: StateFlow<ProfileState> = _state

    fun load(id: String) {
        viewModelScope.launch {
            _state.value = try {
                ProfileState.Loaded(repository.loadProfile(id))
            } catch (e: IOException) {
                ProfileState.Error(e.message)
            }
        }
    }
}
```

Avoid **`GlobalScope`**. Its coroutines aren't tied to anything, so they keep running after the user leaves the screen, can leak memory, and are hard to test. Most old tutorials (including my 2019 post) used it because it was the shortest thing that compiled.

## Dispatchers: which thread runs the work

A **dispatcher** decides which thread or thread pool a coroutine runs on:

| Dispatcher | Use it for |
|---|---|
| `Dispatchers.Main` | UI work and anything that touches views or Compose state |
| `Dispatchers.IO` | Blocking I/O: files, raw sockets, legacy blocking APIs |
| `Dispatchers.Default` | CPU-heavy work: parsing large JSON, sorting, image processing |

`viewModelScope` and `lifecycleScope` start on `Dispatchers.Main`. To move a block elsewhere, use `withContext`:

```kotlin
suspend fun parseReport(raw: String): Report =
    withContext(Dispatchers.Default) {
        heavyParse(raw)
    }
```

The rule worth following is **main-safety**: a suspend function should be safe to call from the main thread, and it should switch dispatchers itself if it needs to. Room, Retrofit and Ktor already do this, so you don't wrap their suspend calls in `withContext(Dispatchers.IO)`.

## Structured concurrency

Coroutines started inside another coroutine become its **children**. The parent doesn't finish until all its children finish, and cancelling the parent cancels the children. This is what "structured concurrency" means, and it's why coroutines don't leak the way threads or callbacks do.

`coroutineScope` creates a child scope inside a suspend function. Combined with `async`, it's the standard way to run things in parallel:

```kotlin
suspend fun loadDashboard(): Dashboard = coroutineScope {
    val profile = async { api.fetchProfile() }
    val feed = async { api.fetchFeed() }
    Dashboard(profile.await(), feed.await())
}
```

Both requests run at the same time. If one fails, the other is cancelled and the exception propagates to the caller, so you never end up with half a dashboard and a request still running in the background.

`runBlocking` looks similar but blocks the current thread until its body finishes. It exists to bridge blocking code (like a `main` function or an old test) into coroutines. Don't use it in app code.

## Cancellation is cooperative

Cancelling a coroutine doesn't kill it. It sets a flag, and the coroutine stops the next time it reaches a **suspension point**. All suspend functions from `kotlinx.coroutines` (`delay`, `withContext`, `Flow.collect` and others) check for cancellation, so most code cancels correctly without any effort.

A tight loop of plain computation never suspends, though, so it won't notice. Check explicitly:

```kotlin
suspend fun hashAll(files: List<File>): List<String> = withContext(Dispatchers.Default) {
    files.map { file ->
        ensureActive() // throws CancellationException if the scope was cancelled
        sha256(file)
    }
}
```

One trap: cancellation is delivered as a `CancellationException`. If you catch `Exception` broadly and swallow it, the coroutine keeps running after it should have stopped. Catch specific exceptions, or rethrow `CancellationException`.

## Exceptions

How an exception travels depends on the builder:

- **`launch`** treats an uncaught exception as a failure of the coroutine. It propagates to the parent, cancels the parent and its other children, and, if nothing handles it, crashes the app on Android. A `try`/`catch` *around* `launch` doesn't help, because `launch` returns immediately. Catch inside the coroutine instead, as in the `ViewModel` above.
- **`async`** holds the exception until you call `await()`, where it's rethrown. (Inside `coroutineScope`, it still cancels the siblings right away.)

When one failing child shouldn't cancel the others, use **`supervisorScope`** (or a `SupervisorJob`). `viewModelScope` already uses a `SupervisorJob`, so one failed `launch` doesn't cancel the rest of the `ViewModel`'s work.

```kotlin
suspend fun syncAll(accounts: List<Account>) = supervisorScope {
    accounts.forEach { account ->
        launch {
            try {
                sync(account)
            } catch (e: IOException) {
                log("Sync failed for ${account.id}: ${e.message}")
            }
        }
    }
}
```

A `CoroutineExceptionHandler` is a last-resort hook for logging uncaught exceptions in a root scope. It doesn't let you recover, so prefer handling errors where they happen.

## Streams of values: Flow

A suspend function returns one value. For a stream of values over time (database changes, location updates, UI state), use **Flow**. In practice, a `ViewModel` exposes a `StateFlow` and the UI collects it:

```kotlin
@Composable
fun ProfileScreen(viewModel: ProfileViewModel) {
    val state by viewModel.state.collectAsStateWithLifecycle()
    ProfileContent(state)
}
```

`collectAsStateWithLifecycle()` stops collecting when the app goes to the background, so you don't keep doing work for a screen nobody sees. In the View system, `repeatOnLifecycle(Lifecycle.State.STARTED)` inside `lifecycleScope` does the same job.

Channels also exist for passing values between coroutines, but in app code you'll reach for `Flow` far more often.

## Testing

`kotlinx-coroutines-test` gives you `runTest`, which runs a test in a coroutine and skips `delay` calls using virtual time, so a test with a five-second timeout finishes instantly:

```kotlin
@Test
fun retriesThenSucceeds() = runTest {
    val api = FakeApi(failuresBeforeSuccess = 2)
    val result = fetchWithRetry(api, retryDelayMillis = 5_000)
    assertEquals("ok", result)
    assertEquals(3, api.calls)
}
```

To make code testable, inject dispatchers instead of hard-coding `Dispatchers.IO` deep inside a class. In `ViewModel` tests, replace `Dispatchers.Main` with `Dispatchers.setMain(StandardTestDispatcher())` in a test rule, since there's no Android main thread on the JVM.

## Quick reference

- Mark async work as `suspend` and make it main-safe.
- Launch from `viewModelScope`, `lifecycleScope` or Compose effects. Never `GlobalScope`.
- Use `withContext` to change dispatcher, and `coroutineScope` + `async` for parallel work.
- Don't swallow `CancellationException`.
- Catch exceptions inside `launch`, and use `supervisorScope` when children should fail independently.
- Expose state as `StateFlow` and collect it with lifecycle awareness.
- Test with `runTest` and injected dispatchers.

The <a href="https://kotlinlang.org/docs/coroutines-guide.html" target="_blank" rel="noopener noreferrer" title="Kotlin coroutines guide">Kotlin coroutines guide</a> covers the library in depth, and Android's <a href="https://developer.android.com/kotlin/coroutines/coroutines-best-practices" target="_blank" rel="noopener noreferrer" title="Best practices for coroutines in Android">coroutines best practices</a> page is a good checklist for app code. For background work that must run even after the app closes, coroutines aren't enough on their own; that's what <a href="https://maikotrindade.com/2019/02/03/introduction-android-work-manager.html" target="_blank" rel="noopener" title="Android WorkManager guide">WorkManager</a> is for.

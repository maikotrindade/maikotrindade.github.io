---
layout: post
title: "Untangling State and Side Effects in Jetpack Compose"
seo_title: "Jetpack Compose State and Side Effects, Untangled"
categories: android compose development
last_modified_at: 2026-11-17
tags: [JetpackCompose, Android, State, StateHoisting, ViewModel, LaunchedEffect, DisposableEffect]
description: "Jetpack Compose state and side effects: remember, state hoisting, state holders, ViewModel with StateFlow, LaunchedEffect, DisposableEffect and when each runs."
published: true
redirect_from:
  - /2025/01/28/execution-order-in-jetpack-compose.html
---

State is any value that can change over time and should change what the user sees: the text in a field, whether a button is enabled, the list on screen. In Jetpack Compose, the UI is a function of state, so when state changes, Compose **recomposes** the parts of the UI that read it. This guide covers where state should live (inside a composable, hoisted to a parent, in a state holder or in a `ViewModel`) and how side effects like `LaunchedEffect` and `DisposableEffect` fit into the composition lifecycle.

I've merged an earlier post on the execution order of effects into this one, since you can't really understand effects without understanding state.

## State inside a composable

The smallest unit is state a composable keeps for itself:

```kotlin
@Composable
fun Counter() {
    var count by remember { mutableStateOf(0) }
    Button(onClick = { count++ }) {
        Text("Clicked $count times")
    }
}
```

Two pieces work together here. `mutableStateOf` creates an observable value: Compose tracks which composables read it and recomposes them when it changes. `remember` keeps that value across recompositions; without it, `count` would reset to `0` every time the function ran.

`remember` doesn't survive configuration changes (rotation, dark mode) or process death. For small UI state that should, like a selected tab or a text field, use **`rememberSaveable`**, which stores the value in the saved instance state.

## State hoisting

Internal state is fine until another part of the UI needs it. A checkbox that tracks its own "checked" value can't tell its parent, and the parent can't reset it.

**State hoisting** moves the state up to the caller. The component receives the current value and reports events through a callback:

```kotlin
@Composable
fun NewsletterCheckbox(
    isChecked: Boolean,
    onCheckedChange: (Boolean) -> Unit
) {
    Row(verticalAlignment = Alignment.CenterVertically) {
        Checkbox(checked = isChecked, onCheckedChange = onCheckedChange)
        Text("Send me the weekly newsletter")
    }
}

@Composable
fun SignUpForm() {
    var subscribed by rememberSaveable { mutableStateOf(false) }
    NewsletterCheckbox(
        isChecked = subscribed,
        onCheckedChange = { subscribed = it }
    )
}
```

The pattern is called **unidirectional data flow**: state flows down as parameters, events flow up as lambdas. `NewsletterCheckbox` is now stateless, so it's easy to preview, test and reuse, and there's a single source of truth for `subscribed`.

A useful rule: hoist state to the **lowest common parent** of everything that reads or changes it. Not higher.

## State holders

When a screen has several related pieces of state and some logic around them, a pile of `var`s in the composable gets hard to follow. Move them into a plain class:

```kotlin
class LoginFormState {
    var username by mutableStateOf("")
        private set
    var password by mutableStateOf("")
        private set

    val canSubmit: Boolean
        get() = username.isNotBlank() && password.length >= 8

    fun onUsernameChange(value: String) { username = value }
    fun onPasswordChange(value: String) { password = value }
}

@Composable
fun rememberLoginFormState() = remember { LoginFormState() }

@Composable
fun LoginForm(
    onSubmit: (String, String) -> Unit,
    state: LoginFormState = rememberLoginFormState()
) {
    Column {
        TextField(
            value = state.username,
            onValueChange = state::onUsernameChange,
            label = { Text("Username") }
        )
        TextField(
            value = state.password,
            onValueChange = state::onPasswordChange,
            label = { Text("Password") },
            visualTransformation = PasswordVisualTransformation()
        )
        Button(
            onClick = { onSubmit(state.username, state.password) },
            enabled = state.canSubmit
        ) {
            Text("Log in")
        }
    }
}
```

The composable only describes the layout, and the rules ("submit needs a username and an 8-character password") live in one class you can unit test without any UI. The `private set` keeps changes going through the class's functions.

## ViewModel: state that outlives the screen

A plain state holder lives as long as the composable that remembers it. When state has to survive configuration changes, or comes from the data layer (network, database), use a **`ViewModel`**. Expose an immutable `StateFlow` and collect it in the UI:

```kotlin
data class ProfileUiState(
    val isLoading: Boolean = true,
    val name: String = "",
    val error: String? = null
)

class ProfileViewModel(private val repository: ProfileRepository) : ViewModel() {
    private val _uiState = MutableStateFlow(ProfileUiState())
    val uiState: StateFlow<ProfileUiState> = _uiState.asStateFlow()

    fun load(userId: String) {
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true, error = null) }
            try {
                val name = repository.fetchName(userId)
                _uiState.update { it.copy(isLoading = false, name = name) }
            } catch (e: IOException) {
                _uiState.update { it.copy(isLoading = false, error = "Couldn't load profile") }
            }
        }
    }
}

@Composable
fun ProfileRoute(viewModel: ProfileViewModel, userId: String) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    LaunchedEffect(userId) { viewModel.load(userId) }
    ProfileScreen(uiState)
}
```

Notice the split: `ProfileRoute` connects to the `ViewModel`, and `ProfileScreen` just takes a `ProfileUiState`. The screen stays stateless and previewable, and you can test the `ViewModel` without Compose.

### Which one to use

| Where state lives | Use it when |
|---|---|
| `remember` / `rememberSaveable` in the composable | Only this composable cares about it (an expanded/collapsed flag, an animation) |
| Hoisted to a parent | Siblings or the parent need to read or change it |
| Plain state holder class | Several related values with UI logic, scoped to part of the UI |
| `ViewModel` | Screen-level state, data from the data layer, or anything that must survive configuration changes |

## Side effects and when they run

A composable should only describe UI. It can run many times, in any order, and Compose may skip it entirely if its inputs didn't change. So anything that reaches outside (starting a request, registering a listener, logging an analytics event) can't go directly in the function body. That's what **effect handlers** are for.

It helps to picture the lifecycle of a composable in three moments: it **enters** the composition, it **recomposes** zero or more times when the state it reads changes, and it **leaves** the composition. Effects hook into those moments.

### LaunchedEffect: run suspend work while on screen

`LaunchedEffect` starts a coroutine when the composable enters the composition. If one of its **keys** changes, the running coroutine is cancelled and a new one starts. When the composable leaves, the coroutine is cancelled.

```kotlin
@Composable
fun SearchResults(query: String, onSearch: suspend (String) -> Unit) {
    LaunchedEffect(query) {
        delay(300) // debounce typing
        onSearch(query)
    }
}
```

Each keystroke changes `query`, which cancels the previous search and starts a new one 300 ms later. The analogy I like: lighting a candle when you enter a room. Change rooms (the key) and you blow it out and light a new one; leave and it's blown out.

Pick keys carefully. `LaunchedEffect(Unit)` runs once per time the composable enters the composition. A key that changes on every recomposition restarts the effect constantly.

### DisposableEffect: set up and clean up

`DisposableEffect` is for things that need cleanup: listeners, callbacks, observers. Its body runs on enter (and on key change), and its `onDispose` block runs on leave (and before re-running on key change).

```kotlin
@Composable
fun LifecycleLogger(lifecycleOwner: LifecycleOwner, onEvent: (Lifecycle.Event) -> Unit) {
    DisposableEffect(lifecycleOwner) {
        val observer = LifecycleEventObserver { _, event -> onEvent(event) }
        lifecycleOwner.lifecycle.addObserver(observer)
        onDispose {
            lifecycleOwner.lifecycle.removeObserver(observer)
        }
    }
}
```

Think of hotel housekeeping: the room is set up when you check in, and cleaned when you check out or switch rooms. `onDispose` is required, which is a nice guard against forgetting the cleanup.

### SideEffect and rememberUpdatedState

**`SideEffect`** runs after every successful recomposition. Use it to push Compose state into something that isn't Compose, like an analytics SDK's current screen.

**`rememberUpdatedState`** solves a subtle problem: a long-running effect that captures a lambda keeps the *first* version of it. Wrap the value so the effect always sees the latest one without restarting:

```kotlin
@Composable
fun SplashScreen(onTimeout: () -> Unit) {
    val currentOnTimeout by rememberUpdatedState(onTimeout)
    LaunchedEffect(Unit) {
        delay(2_000)
        currentOnTimeout()
    }
}
```

### The order, side by side

| | Runs | Re-runs | Cleans up |
|---|---|---|---|
| Composable body | On enter | On recomposition, when state it reads changes | When it leaves |
| `LaunchedEffect(key)` | After entering | When a key changes (old coroutine cancelled) | Cancelled when it leaves |
| `DisposableEffect(key)` | After entering | When a key changes (`onDispose` first) | `onDispose` when it leaves |
| `SideEffect` | After each successful composition | Every recomposition | Nothing to clean up |

Effects run *after* the composition is applied, never in the middle of it. So a composable's body always runs before its effects, and an effect never sees a half-built UI.

## A few rules of thumb

- Keep composables as stateless as you can and hoist state to the lowest common parent.
- Put logic in state holders or `ViewModel`s, not in composable bodies.
- Expose `StateFlow` from `ViewModel`s and collect with `collectAsStateWithLifecycle()`.
- Never start work directly in a composable body. Use `LaunchedEffect` for suspend work and `DisposableEffect` for anything that needs cleanup.
- Choose effect keys deliberately, and use `rememberUpdatedState` for callbacks inside long-lived effects.

Android's guides on <a href="https://developer.android.com/develop/ui/compose/state" target="_blank" rel="noopener noreferrer" title="State and Jetpack Compose, Android Developers">state</a> and <a href="https://developer.android.com/develop/ui/compose/side-effects" target="_blank" rel="noopener noreferrer" title="Side-effects in Compose, Android Developers">side effects</a> go deeper. If you're coming from React, my post on <a href="https://maikotrindade.com/android/react-native/2026/04/25/jetpack-compose-react-native-similarities.html" target="_blank" rel="noopener" title="Jetpack Compose and React Native similarities">Jetpack Compose and React Native similarities</a> maps `useState` and `useEffect` to the APIs above.

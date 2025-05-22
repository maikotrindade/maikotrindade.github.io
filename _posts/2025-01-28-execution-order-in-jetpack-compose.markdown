---
published: true
title: Execution Order in Jetpack Compose Explained with Analogies
layout: post
---

Understanding when `LaunchedEffect`, `DisposableEffect`, and composables run in Jetpack Compose can be tricky. Let’s simplify with a few real-world analogies.

### 🎭 Composables = Stage Actors

Composables are like actors:

- They enter when the screen appears.

- They update their lines when state changes (recomposition).

- They exit when removed from the UI.

### 🕯️ LaunchedEffect = Candle in a Room

- You light a candle when entering a room → `LaunchedEffect` runs.

- If the room changes (key changes), you blow it out and light a new one.

- If you leave, the candle is blown out.

- Use it for one-time effects or state collection.

### 🧹 DisposableEffect = Hotel Housekeeping
- Housekeeper sets up the room → `DisposableEffect` runs.

- When you check out (or key changes), the room is cleaned → onDispose is called.

- Perfect for listeners or subscriptions that need cleanup.

### 🔄 Recomposition = Changing Actor’s Lines
If the script (state) changes, actors stay on stage but adjust their lines. No need to re-run effects unless keys change.

### Quick Comparison

| Concept          | Analogy      | When It Runs         | When It Cleans Up     |
| ---------------- | ------------ | -------------------- | --------------------- |
| Composable       | Actor        | On screen draw/state | On removal            |
| LaunchedEffect   | Candle       | On enter/key change  | On key change/removal |
| DisposableEffect | Housekeeping | On enter/key change  | On key change/removal |


### ✅ Final Tip
So next time you add a `LaunchedEffect` or a `DisposableEffect`, ask yourself:

- Is this a one-time action? → Use `LaunchedEffect`.

- Does it need cleanup? → Use `DisposableEffect`.

- Thinking this way makes Compose easier and your code cleaner.

- [Side-Effect] official docs.

- [LaunchedEffect] official docs.

- [DisposableEffect] official docs.

- [RecompositionOverview] official docs.


[Side-Effect]:https://developer.android.com/jetpack/compose/side-effects
[LaunchedEffect]:https://developer.android.com/reference/kotlin/androidx/compose/runtime/LaunchedEffect
[DisposableEffect]:https://developer.android.com/reference/kotlin/androidx/compose/runtime/DisposableEffect
[RecompositionOverview]:https://developer.android.com/jetpack/compose/phases#recomposition

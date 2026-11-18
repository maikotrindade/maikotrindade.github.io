---
redirect_from:
  - /2023/10/05/benefits-of-compose-part-1.html
  - /2023/11/15/benefits-of-compose-part-2.html
published: true
title: "Migrating from XML Views to Jetpack Compose: A Practical Guide"
seo_title: "Migrating from XML Views to Jetpack Compose"
layout: post
last_modified_at: 2026-11-17
tags: [JetpackCompose, Android, Migration, Views, Interoperability, Kotlin]
description: "How to migrate an Android app from XML views to Jetpack Compose step by step: ComposeView, AndroidView, theming, navigation, testing and common pitfalls."
---

You don't migrate an Android app from XML views to Jetpack Compose in one go. You do it screen by screen, sometimes component by component, while the app keeps shipping. Compose was designed for this: a Compose UI can live inside a View layout, and a View can live inside a Compose UI. This guide covers why teams migrate, the order that works, the interop APIs, and the problems you'll run into on the way.

I've led migrations from XML to Compose on production apps, and the lessons below come from that work. This post also replaces two earlier posts on the benefits of Compose, which now redirect here.

## Why migrate

The practical benefits, beyond "it's the new thing":

- **Less code for the same UI.** No XML layouts, no `findViewById` or view binding, no adapters and view holders for lists. A `LazyColumn` with an item composable replaces a `RecyclerView`, an adapter, a view holder and an item layout.
- **UI as a function of state.** You describe what the screen looks like for a given state, and Compose updates it when the state changes. A whole class of bugs where a view wasn't updated goes away.
- **Reuse through functions.** A component is just a function with parameters, so composing and reusing UI is much easier than with custom views or `<include>` layouts.
- **Faster iteration.** Previews and Live Edit in Android Studio show changes without a full rebuild and redeploy.
- **Where Android is going.** New Material 3 components, Wear OS and TV libraries are built for Compose first.

None of these justify a big-bang rewrite. They justify building new UI in Compose and moving old screens over when you touch them anyway.

## The order that works

1. **Set up the foundation.** Add Compose to the build, then create a Compose theme (`MaterialTheme` with your colours, typography and shapes) that matches your existing XML theme. Do this first, so every Compose piece looks right from day one.
2. **Build new features in Compose.** Every new screen is Compose from the start. This stops the amount of XML from growing, and the team learns on fresh code.
3. **Build shared components.** Buttons, text fields, cards and empty states your designers use everywhere. Once these exist in Compose, migrating a screen is mostly assembly.
4. **Migrate simple, low-risk screens.** Settings, about pages, static content. They build confidence without risking core flows.
5. **Migrate complex screens when you're changing them anyway.** If a feature is getting a redesign, that's the time to move it. Rewriting a stable, complex screen just to change its technology is usually poor value.
6. **Move navigation last.** Switching to Navigation Compose is easiest once most screens are composables.

## Interoperability: mixing Views and Compose

### Compose inside a View layout

Use `ComposeView`, in XML or in code. Here's a Fragment that renders Compose:

```kotlin
class ProfileFragment : Fragment() {
    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View = ComposeView(requireContext()).apply {
        setViewCompositionStrategy(ViewCompositionStrategy.DisposeOnViewTreeLifecycleDestroyed)
        setContent {
            AppTheme {
                ProfileScreen()
            }
        }
    }
}
```

The **composition strategy** matters inside Fragments. The default disposes the composition when the view is detached from the window, but a Fragment's view lifecycle is different from its view's attachment. `DisposeOnViewTreeLifecycleDestroyed` ties the composition to the Fragment's view lifecycle, which avoids leaks and lost state.

You can also drop a `ComposeView` into an existing XML layout to migrate one part of a screen, like a header or a single card.

### A View inside Compose

Some Views don't have a Compose equivalent yet, or you rely on a third-party View (a map, an ad, a video player). Wrap them with `AndroidView`:

```kotlin
@Composable
fun LegacyChart(points: List<Float>, modifier: Modifier = Modifier) {
    AndroidView(
        modifier = modifier,
        factory = { context -> LineChartView(context) },
        update = { chart -> chart.setPoints(points) }
    )
}
```

`factory` runs once to create the View, and `update` runs whenever the state it reads changes. Keep the View's state flowing from Compose into the View through `update`, not the other way round. If you already have an XML layout, `AndroidViewBinding` lets you inflate it with view binding inside Compose.

## Things that will bite you

### Two themes during the transition

Until the migration is done, the XML theme and the Compose theme both exist and have to match. Define colours and dimensions in one place and reference them from both, and review new Compose screens next to old XML ones. Small differences in text styles are the most common thing designers notice.

### State that lived in Views

Views kept some state themselves: the text in an `EditText`, the scroll position of a `RecyclerView`, which tab was selected. In Compose, you own that state. Hoist it to a `ViewModel` or use `rememberSaveable`, or users will lose their input on rotation. My post on <a href="https://maikotrindade.com/android/compose/development/2025/03/08/untangling-state-android-app-management.html" target="_blank" rel="noopener" title="State and side effects in Jetpack Compose">state and side effects in Compose</a> covers where state should live.

### Lifecycle code in the wrong place

Code in `onResume` or `onStart` that touches views needs a new home. Lifecycle-aware Flow collection (`collectAsStateWithLifecycle`) and effects like `LaunchedEffect` and `DisposableEffect` replace most of it.

### Performance surprises

Compose is fast, but a few habits from the View world hurt it: doing heavy work inside a composable body (it can run on every recomposition), passing unstable types like plain `List` from data classes the compiler can't prove are stable, and reading state higher up than needed so too much recomposes. Use Layout Inspector's recomposition counts to find hot spots, and test performance with release builds and Baseline Profiles. Debug builds are much slower.

### Tests

Espresso tests keep working for View screens, and Compose tests (`createAndroidComposeRule`) can find both composables and Views in a mixed screen. Add test tags or content descriptions while migrating. They make tests more robust, and good content descriptions make the screen <a href="https://maikotrindade.com/2024/12/03/a-guide-to-accessibiliy-in-android-apps-jetpack-compose.html" target="_blank" rel="noopener" title="Accessibility in Android apps with Jetpack Compose">accessible</a> too.

## Measuring progress

Track the migration so it doesn't stall halfway. Simple metrics are enough: the number of XML layout files, the number of screens fully in Compose, and APK size. Celebrate when a dependency like the RecyclerView or Fragment library can finally be removed.

A migration is finished when nobody has to think about two UI systems anymore. Until then, the rule that keeps it moving is simple: anything new is Compose, and anything you touch moves to Compose if it's cheap to do.

Android's <a href="https://developer.android.com/develop/ui/compose/migrate" target="_blank" rel="noopener noreferrer" title="Migrate to Jetpack Compose, Android Developers">migration guide</a> and <a href="https://developer.android.com/develop/ui/compose/migrate/interoperability-apis" target="_blank" rel="noopener noreferrer" title="Compose and Views interoperability APIs">interoperability API reference</a> cover more edge cases, like using Compose in RecyclerView items.

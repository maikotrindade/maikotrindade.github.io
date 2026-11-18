---
published: true
title: "Kotlin Multiplatform for Android and iOS: A Practical Introduction"
seo_title: "Kotlin Multiplatform for Android & iOS Apps"
layout: post
last_modified_at: 2026-11-17
tags: [KotlinMultiplatform, KMP, Kotlin, Android, iOS, ComposeMultiplatform]
description: "Kotlin Multiplatform for Android and iOS: shared modules, expect/actual, libraries, calling Kotlin from Swift, Compose Multiplatform and when to choose it."
---

Kotlin Multiplatform (KMP) lets you write code once in Kotlin and use it on Android, iOS, desktop, web and server. For mobile apps, the usual approach is to share the business logic (networking, data storage, validation, state) and keep each platform's UI native, though you can also share the UI with Compose Multiplatform. This guide explains how a KMP project is structured, how shared code reaches each platform, the libraries you'll use, and when KMP is a better fit than React Native or Flutter.

I first wrote about KMP in 2024, mostly listing its benefits. Since then it has matured a lot, so I rewrote the post to show how it actually works.

## Where KMP stands

- KMP has been **stable** since Kotlin 1.9.20 in late 2023.
- Google **officially supports** KMP for sharing business logic between Android and iOS, and several Jetpack libraries now publish multiplatform versions, including Room, DataStore, ViewModel and Lifecycle.
- **Compose Multiplatform** for iOS reached stable in 2025, so sharing UI is now a supported option too.

## How a project is structured

A typical mobile KMP project has three parts:

```
my-app/
├── shared/                 # Kotlin Multiplatform module
│   └── src/
│       ├── commonMain/     # code for all platforms
│       ├── androidMain/    # Android-specific implementations
│       └── iosMain/        # iOS-specific implementations
├── androidApp/             # regular Android app, depends on :shared
└── iosApp/                 # Xcode project, uses the shared framework
```

The Kotlin compiler builds `shared` into a normal Android library for the Android app (running on the JVM/ART) and into a native **framework** for iOS through Kotlin/Native. Your iOS code imports that framework like any other Swift dependency. There's no JavaScript bridge and no runtime interpreter: on iOS, shared Kotlin code is compiled to native machine code.

Most of your code goes in `commonMain`, which can only use multiplatform libraries and the Kotlin standard library. Platform folders exist for the parts that genuinely differ.

## expect and actual

When common code needs something only the platform provides, declare it with `expect` in `commonMain` and implement it with `actual` in each platform folder:

```kotlin
// commonMain
expect fun platformName(): String

class Greeting {
    fun greet(): String = "Hello from ${platformName()}"
}
```

```kotlin
// androidMain
actual fun platformName(): String = "Android ${android.os.Build.VERSION.SDK_INT}"
```

```kotlin
// iosMain
import platform.UIKit.UIDevice

actual fun platformName(): String =
    UIDevice.currentDevice.systemName() + " " + UIDevice.currentDevice.systemVersion
```

In `iosMain`, you can call Apple's frameworks (UIKit, Foundation and others) directly from Kotlin. In practice, I'd keep `expect`/`actual` for small, low-level pieces. For bigger platform differences, define an interface in common code and pass in a platform implementation, which is easier to test and to fake.

## Libraries you'll actually use

You can't use Android-only or JVM-only libraries (Retrofit, Gson, OkHttp) in `commonMain`. The multiplatform equivalents:

| Need | Library |
|---|---|
| HTTP client | Ktor client |
| JSON | kotlinx.serialization |
| Async | kotlinx.coroutines and Flow |
| Database | Room (multiplatform) or SQLDelight |
| Key-value storage | DataStore |
| Dates and times | kotlinx-datetime |
| Dependency injection | Koin, or manual DI |
| Shared ViewModels | androidx.lifecycle ViewModel |

A shared repository then looks like ordinary Kotlin:

```kotlin
@Serializable
data class Article(val id: String, val title: String)

class ArticleRepository(private val client: HttpClient) {
    suspend fun latest(): List<Article> =
        client.get("https://api.example.com/articles").body()
}
```

## Calling shared code from Swift

From Swift, the shared module looks like an Objective-C framework. Classes, functions and data classes work as you'd expect. A few things need attention:

- **Suspend functions** are exposed to Swift as `async` functions (and as completion handlers), so `try await repository.latest()` works.
- **Flows** don't map to anything in Swift out of the box. Most teams use SKIE or KMP-NativeCoroutines, which turn them into Swift `AsyncSequence`s.
- **Sealed classes, generics and default arguments** lose some of their expressiveness on the way through Objective-C. SKIE fixes several of these. JetBrains is also working on direct Swift export, which will remove the Objective-C layer.

That interop layer is where iOS developers on the team will form their opinion of KMP, so it's worth making the shared API pleasant to use from Swift.

## Sharing UI with Compose Multiplatform

With **Compose Multiplatform**, the same Compose code you write for Android can render on iOS, desktop and web. If your team already writes Jetpack Compose, the learning curve is small.

You don't have to choose all or nothing. A common path is to share logic first, keep native UIs, and then share individual screens where the design is the same on both platforms. Compose screens can be embedded in a SwiftUI app and SwiftUI views in a Compose screen.

## KMP compared with React Native and Flutter

I work with both Kotlin and React Native, and they solve different problems:

| | KMP | React Native | Flutter |
|---|---|---|---|
| Language | Kotlin | TypeScript/JavaScript | Dart |
| What's shared | Logic by default, UI optional | Logic and UI | Logic and UI |
| UI | Native, or Compose Multiplatform | Native components driven from JS | Its own rendering engine |
| Adopting in an existing native app | Module by module | Possible but more work | Possible but more work |
| Best fit | Teams with Android/Kotlin skills, apps with existing native code | Teams with web/React skills | Teams starting fresh that want one UI everywhere |

KMP's biggest practical advantage is **incremental adoption**. You can add one shared module (say, your API client and models) to an existing Android and iOS app without rewriting anything else. That's much harder to do with React Native or Flutter, which want to own the screen.

## When to choose KMP

KMP is a good choice when:

- your team already knows Kotlin, especially Android developers;
- you have existing native Android and iOS apps and want to stop writing the same logic twice;
- you want native UIs, or want to decide screen by screen whether to share UI;
- you need direct access to platform APIs without writing bridges.

It's a weaker fit when your team is mostly web developers (React Native will feel more natural), or when your iOS team doesn't want to work with Kotlin at all. KMP works best when both platforms' developers treat the shared module as their code.

The official <a href="https://kotlinlang.org/docs/multiplatform/get-started.html" target="_blank" rel="noopener noreferrer" title="Get started with Kotlin Multiplatform">Kotlin Multiplatform getting started guide</a> sets up a project in a few minutes. If you're weighing KMP against React Native, my post on <a href="https://maikotrindade.com/android/react-native/2026/04/25/jetpack-compose-react-native-similarities.html" target="_blank" rel="noopener" title="Jetpack Compose and React Native similarities">Jetpack Compose and React Native similarities</a> compares the two UI models.

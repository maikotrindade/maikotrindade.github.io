---
published: true
title: Koin – Dependency Injection for Kotlin
layout: post
---

### Intro
[Koin] is a lightweight dependency injection library for Kotlin and written in pure Kotlin. using functional resolution only: no proxy, no code generation, no reflection. Koin is a DSL, using Kotlin’s DSLs, that describes your dependencies into modules and sub-modules. You describe your definitions with certain key functions that mean something in the Koin context. 

<img src="http://maikotrindade.github.io/public/img/ci.png" width="320" height="320" alt="Koin DI"/>

In this article, we are going to pass through the basic steps to setup and take advantage of dependency injection with Koin for a simple project.

### 1. Setup

>	// Add Jcenter to your repositories if needed
>	repositories {
>	    jcenter()
>	}
>	dependencies {
>	    // Koin for Android
>	    implementation 'org.koin:koin-android:{revnumber}'
>	}

### 2. Declare a module
Defines those entities which will be injected in the app.

>	val appModule = module {
>		single { DataRepository }
>	}

### 3. Use Application layer to initialize Koin injection
Trigger the DI process and indicate which modules will be available when needed

>	class BaseApplication : Application() {
>	
>	  override fun onCreate() {
>	    super.onCreate()
>	    startKoin(this, appModule)
>	  }
>	
>	}

### 4. Use the actual injection

>	class MainActivity : AppCompatActivity() {
>	  private val repository: DataRepository by inject()
>	  ...
>	}

This was the basic usage of koin which has much more power/features available in its framework. Another great Koin feature is the integration with the Architecture Component View Model. Koin has a specif project called `koin-android-viewmodel` project is dedicated to inject Android Architecture ViewModel. 

### Architecture Components with Koin: ViewModel

### 1. Setup
>	// Add Jcenter to your repositories if needed
>	repositories {
>	    jcenter()
>	}
>	dependencies {
>	    // ViewModel for Android
>	    implementation 'org.koin:koin-android-viewmodel:{revnumber}'
>	    // or ViewModel for AndroidX
>	    implementation 'org.koin:koin-androidx-viewmodel:{revnumber}'
>	}

### 2. Declare a module for your viewModule
>	val appModule = module {
>	    // ViewModel for News View with a dependency in its constructor
>	    viewModel { NewsViewModel(get()) }
>	}

### 3. Use the actual injection

>	class MainActivity() : AppCompatActivity() {
>	
>	  // lazy inject MyViewModel
>	  val viewModel : NewsViewModel by viewModel()
>	}

### Koin Key Functions

* `module { }` - create a Koin Module or a submodule (inside a module)
* `factory { }` - provide a factory bean definition
* `single { }` - provide a bean definition
* `get()` - resolve a component dependency
* `bind` - additional Kotlin type binding for given bean definition
* `getProperty()` - resolve a property

### Futher Details
I highly recommend the [official docs] and the following articles: [Koin - Simple Android DI] and [Ready for Koin 2.0] by [Arnaud Giuliani]

[Koin]: https://insert-koin.io/
[Koin - Simple Android DI]: https://android.jlelse.eu/koin-simple-android-di-a47827a707ce
[Ready for Koin 2.0]: https://medium.com/koin-developers/ready-for-koin-2-0-2722ab59cac3
[Arnaud Giuliani]: https://github.com/arnaudgiuliani
[official docs]: https://insert-koin.io/docs/2.0/documentation/koin-android/index.html

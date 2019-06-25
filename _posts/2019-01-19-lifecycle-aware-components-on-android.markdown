---
published: true
title: Lifecycle-aware components on Android
layout: post
---

### Introduction

[Lifecycle-aware] components perform actions in response to a change in the lifecycle status of another component, such as activities and fragments. These components help you produce better-organized, and often lighter-weight code, that is easier to maintain.

A common pattern is to implement the actions of the dependent components in the lifecycle methods of activities and fragments. However, this pattern leads to a poor organization of the code and to the proliferation of errors. By using lifecycle-aware components, you can move the code of dependent components out of the lifecycle methods and into the components themselves.

### Components

**ViewModel** - provides a way to create and retrieve objects that are bound to a specific lifecycle. A ViewModel typically stores the state of a view's data and communicates with other components, such as data repositories or the domain layer which handles business logic. To read an introductory guide to this topic, see ViewModel.

**LifecycleOwner/LifecycleRegistryOwner** - both LifecycleOwner and LifecycleRegistryOwner are interfaces that are implemented in the AppCompatActivity and Support Fragment classes. You can subscribe other components to owner objects which implement these interfaces, to observe changes to the lifecycle of the owner. To read an introductory guide to this topic, see Handling Lifecycles.

**LiveData** - allows you to observe changes to data across multiple components of your app without creating explicit, rigid dependency paths between them. LiveData respects the complex lifecycles of your app components, including activities, fragments, services, or any LifecycleOwner defined in your app. LiveData manages observer subscriptions by pausing subscriptions to stopped LifecycleOwner objects, and cancelling subscriptions to LifecycleOwner objects that are finished. To read an introductory guide to this topic, see LiveData.
 
#### Lifecycle

[Lifecycle] is a class that holds the information about the lifecycle state of a component (like an activity or a fragment) and allows other objects to observe this state. Lifecycle uses two main enumerations to track the lifecycle status for its associated component:

**Event** – The lifecycle events that are dispatched from the framework and the Lifecycle class. These events map to the callback events in activities and fragments.
**State** – The current state of the component tracked by the Lifecycle object.

#### LifecycleOwner

[LifecycleOwner] is a single method interface that denotes that the class has a Lifecycle. It has one method, getLifecycle(), which must be implemented by the class. If you're trying to manage the lifecycle of a whole application process instead, see ProcessLifecycleOwner.

This interface abstracts the ownership of a Lifecycle from individual classes, such as Fragment and AppCompatActivity, and allows writing components that work with them. Any custom application class can implement the LifecycleOwner interface.

Components that implement LifecycleObserver work seamlessly with components that implement LifecycleOwner because an owner can provide a lifecycle, which an observer can register to watch.

[Lifecycle-aware]: https://developer.android.com/topic/libraries/architecture/lifecycle
[Lifecycle]: https://developer.android.com/reference/androidx/lifecycle/Lifecycle.html
[LifecycleOwner]: https://developer.android.com/reference/androidx/lifecycle/LifecycleOwner.html
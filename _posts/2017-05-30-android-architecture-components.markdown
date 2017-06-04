---
published: true
title: Lets make Android great again: Architecture Components
layout: post
---
<img src="http://maikotrindade.github.io/public/img/android_great_again.jpg" height="360" width="640" alt="Android great again"/>
Google I/O 2017 brought a new package of outstanding news. In my point of view, one of the most relevant news were [Architecture components](https://developer.android.com/topic/libraries/architecture/index.html), a new bunch of libraries that help developers design apps with testability, maintainability and clean code.

### Room
This is my favorite library of Architecture Components, surely. Room is an object mapping library that let the code clean and collaborate with SQL queries. Furthermore, the library provides SQL queries validation compilation time, annotations and [observables](http://reactivex.io/documentation/observable.html) for database changes. I knew this today would come, a day that Google will release a library for persistence such Apple offer for iOS ([Core Data](https://developer.apple.com/library/content/documentation/Cocoa/Conceptual/CoreData/)). Hereafter I have no doubt Room will be a reference for the persistence layer although there are tons of similar libraries such as [ORMLite](http://ormlite.com/), [Active Android](http://www.activeandroid.com/) or [GreenDAO](http://greenrobot.org/greendao/).

### ViewModel
* Provide data for fragment/activity;
* Independent of View: configuration changes don't affect ViewModel;
* Similar to an usual presenter however the retention/loading is built-in;
* Retention happens through FragmentManager and HolderFragment;

### Live Data
it is responsible for listen and propagate data changes: an observable data holder It allows broadcasting of data changes all over the architecture layers taking into account all system issues eg. memory leaks. 

### Lifecycle Owner - Lifecycle
It allows the creation of lifecycle-aware components which are able to adjust itself automatically according to the current lifecycle. This feature is possible because Lifecycle owner associates a class to the lifecycle via an abstract class called getLifecycle().

#### Further Details
I recommend this [project](https://github.com/googlesamples/android-architecture-components) which Google team implemented samples of Architecture Componentes and this [video](https://www.youtube.com/watch?v=FrteWKKVyzI&list=PLOU2XLYxmsIKC8eODk_RNCWv3fBcLvMMy&index=13) from Google I/O.

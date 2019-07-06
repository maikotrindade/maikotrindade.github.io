---
published: true
title: Dependency Injection with Dagger 2
layout: post
---

### Introduction

Dependency Injection (DI) is a design pattern that removes the dependency from the programming code so that it can be easy to manage and test the application. Dependency Injection makes our programming code loosely coupled. DI allows classes to define their dependencies without constructing them. At runtime, another class is responsible for providing these dependencies.

Problems of Dependency
There are mainly two problems of dependency lookup: 

 - tight coupling The dependency lookup approach makes the code tightly coupled. If resource is changed, we need to perform a lot of modification in the code.

 - Not easy for testing This approach creates a lot of problems while testing the application especially in black box testing.

### Dagger 2 

Dagger 2 automatically constructs objects by walking the dependency tree, and it provides compile-time guarantees on dependencies.
Dagger 2 is also recommended by [Android team].

Dagger 2 uses the following annotations:

`@Module` and `@Provides`: define classes and methods which provide dependencies. `@Module` are responsible for providing objects which can be injected. Such classes can define methods annotated with `@Provides`. The returned objects from these methods are available for dependency injection.

`@Inject`: requests the dependencies. In other words, this annotation will let Dagger knows what the dependencies it is needed to be used by the dependant. 
Can be used on a constructor, a field, or a method.

`@Component`: enables selected modules and used for performing dependency injection.


### Further Details

[The Future of Dependency Injection with Dagger 2] by Jake Wharton
[DAGGER 2 - A New Type of dependency injection]

[The Future of Dependency Injection with Dagger 2]: https://www.youtube.com/watch?v=plK0zyRLIP8
[Android team]: https://developer.android.com/jetpack/docs/guide#fetch-data
[DAGGER 2 - A New Type of dependency injection]: https://www.youtube.com/watch?v=oK_XtfXPkqw
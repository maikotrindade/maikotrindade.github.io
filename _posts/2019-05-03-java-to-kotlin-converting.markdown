---
published: true
title: Converting Java to Kotlin 
layout: post
---

### Introduction

Google announced official support for the Kotlin language at Google I/O 2017. Many developers started migrating the code base away from Java and learning Kotlin on the way. We are going to discuss how you can go from Java to Kotlin and also talk about some tips about this process.

### Getting started

The very easy/initial thing you could do: use the Android Studio IDE to starting the convertion: 

In the IDE, go to `Android Studio -> Code -> Convert Java File to Kotlin File`:
The converter is really nice, it is smart and does the most of job gracefully. However during the automated process the converter would choose not the most appropriate choice, so you must look into the code and figure out if the converter was right in all the scenarios. Probably the most interesting issue you may face is the nullability, because by default, all the converted object will be non-nullable and you will have to explicitly specified them to be nullable or change your logic. Another issue is about usage of android-annontations will most likely break. There is a shortcut to access the converter: `CMD+SHFT+ALT+K` or `CTRL+SHIFT+ALT+K` depending of your operational system.

Another option of converting the code is using the online tool [try.kotlinlang]. Access the URL [https://try.kotlinlang.org] and click on “Convert from Java”. In this way you can convert your project graduallly and observe all the changes clearly.


<img src="http://maikotrindade.github.io/public/img/javatokotlin.png" width="410" height="380" alt="From Java to Kotlin Android"/>

### Things to keep in mind

Interoperability – Java and Kotlin work perfectly together. So don't be afraid to add Kotlin code step by step, it’s not necessary to migrate all code to another language.
Pitfalls –  Automatic conversions can also be dangerous to your project, there are some scenarios that you may face new bugs in your code, for example an unexpected nullability. Some code converted can be asserted as not null which in turn can lead to a NullPointerException.
Usage of `val` and `lateinit` – the misusage of these can cause problems to your actual project. `val` is like Java `final` variable and it's known as immutable in kotlin and can be initialized only single time. A misusage of this field is setting a variable would be changed somehow, for example, a variable inside your model which will be used in a parcelable or as response of networki request. Make the property nullable if it makes better sense and improves null safety. `lateinit` might be good if used properly but it has its cons as well. Don't make it a replacement for NullPointerException.

### Google Codelab "Refactoring to Kotlin"

Google offers a Codelab specifically for refactoring [Java code to Kotlin]. Besides this course provides a very interesting channel to learn more about Koltin, its features and concepts, this is the list of what you will learn in the codelab:

* Handling nullability
* Implementing singletons
* Data classes
* Handling strings
* Elvis operator
* Destructuring
* Properties and backing properties
* Default arguments and named parameters
* Working with collections
* Extension functions
* Top-level functions and parameters
* let, apply, with, and run keywords

Check the codelab versions in [Chinese] and [Brazilian Portuguese].

[try.kotlinlang]: https://try.kotlinlang.org/
[https://try.kotlinlang.org]: https://try.kotlinlang.org/
[Codelab]: https://codelabs.developers.google.com/codelabs/java-to-kotlin/#0
[Java code to Kotlin]: https://codelabs.developers.google.com/codelabs/java-to-kotlin/#0
[Chinese]: https://codelabs.developers.google.com/codelabs/java-to-kotlin-zh/#0
[Brazilian Portuguese]: https://codelabs.developers.google.com/codelabs/java-to-kotlin-pt-br/#0

---
published: true
title: Improving accessibility of Android app
layout: post
---

### Accessibility tooling on Android

Android has a collection of tools which can help people with disability and the following list has the most important features in my opnion:

#### ✨ Talkback screen reader and Select to Speak 

This feature helps you as you navigate your smartphone. On a given screen, it will tell you what kind of screen it is, and what's on it. For example, if you're on a settings page, Talkback will read out the section name (such as notifications). When you tap an icon or item, your selection gets a green outline, and the assistant identifies it. Double tapping the same icon opens it. Talkback reminds you to double-tap when you tap on an item.

#### ✨ Font Size and High Contrast Text 

This setting lets you change the font size on your device from the default. You can make the text smaller than the default, or various levels larger. As you make adjustments, you can see how it will look.

#### ✨ Magnification 🔍

The user can use a gesture to zoom in on certain parts of your screen. Once you enable the feature in settings, you can zoom in by tapping the screen three times with your finger.

#### ✨Switch Access 

Users can Interact with Android app using one or more switches or a keyboard instead of the touch screen. It is also possible to use Camera Switches to navigate with facial gestures.


### Jetpack Compose & Accessibility

Jetpack Compose is great when it comes [accessibility] - it uses semantics properties to pass information to Accessibility services to transform what’s shown on screen to a more fitting format for a user with a specific need.

Most built-in composables like Text and Button fill these semantics properties with information inferred from the composable and its children. Some modifiers like toggleable and clickable will also set certain semantics properties.

However, sometimes the framework needs more information to understand how to describe a UI element to the user.

<img src="http://maikotrindade.github.io/public/img/mobile-accessibility.png" width="360" height="220" alt="Jetpack compose accessibility"/> 

### Improving accessibility using Jetpack compose

This list is mainly focused on some approaches you should think about while developing the app.

There are a bunch of other items related to UI/UX which weren't included on this list (eg. Colour contrast ratios, minimum touch target sizes, High Contrast theme, etc).

The following items are meant to help people with accessibility needs use the app successfully:

**Describe visual elements**

Pass a textual description of the visual element whenever is relevant.

**Describe click labels**

You can use a click label to add semantic meaning to the click behavior of a composable. This way, accessibility services can explain to the user what will happen when the user interacts with the component.

**Describe an element’s state**

You can describe the state of a component in order to Android to read out the state that the component is in. For example, a toggleable checkbox can be in either a “Checked” or an “Unchecked” state.

**Merge visual elements**

Sometimes you need to merge elements to make Talkback and Switch Access more efficient.
For example if every single low-level visual element in your screen is focused independently, a user will have to interact a lot to move across the screen. Other issue you may face is a user not being able to understand lists of the app because each element of the list will be focused independently (instead of the item itself).

[accessibility]: https://developer.android.com/develop/ui/compose/accessibility

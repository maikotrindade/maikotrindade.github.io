---
published: true
title: "A Guide to Accessibility in Android Apps with Jetpack Compose"
seo_title: "Android Accessibility with Jetpack Compose: A Guide"
layout: post
last_modified_at: 2026-11-17
tags: [Accessibility, JetpackCompose, Android, TalkBack, a11y, Testing]
description: "Android accessibility with Jetpack Compose: TalkBack, Switch Access, semantics, content descriptions, touch targets, contrast and automated a11y tests."
redirect_from:
  - /2024/09/11/improving-accessibility-android-app.html
---

Accessibility on Android means making sure people can use your app with a screen reader, a switch device, voice commands, large fonts or magnification. Jetpack Compose makes most of this easier than the View system did, because accessibility information comes from **semantics** that the built-in components fill in for you. This guide covers how Android's accessibility services see your UI, the Compose APIs that fix the common problems, and how to test for them.

It started as a talk. On November 28, 2024, I presented "Creating Inclusive Experiences: A Guide to Accessibility in Android Apps with Jetpack Compose" at <a href="https://www.meetup.com/the-test-tribe-calgary-meetup/" target="_blank" rel="noopener noreferrer" title="The Test Tribe Calgary meetup group">The Test Tribe's 12th Calgary meetup</a>, hosted at the Neo Financial office. For the demos I built <a href="https://github.com/maikotrindade/InaccessibleApp" target="_blank" rel="noopener noreferrer" title="InaccessibleApp, a demo app with deliberate accessibility issues">InaccessibleApp</a>, a small app full of deliberate accessibility bugs, and fixed them live. This post folds in an earlier article I wrote on Android's accessibility tools, so everything is in one place.

## Why it matters

The <a href="https://www.who.int/news-room/fact-sheets/detail/disability-and-health" target="_blank" rel="noopener noreferrer" title="WHO fact sheet on disability and health">World Health Organization</a> estimates that about 1.3 billion people, roughly 1 in 6, live with a significant disability. Add temporary and situational limits (a broken wrist, bright sunlight, holding a baby in one arm) and accessible design helps far more people than it first seems. In many markets it's also a legal requirement.

## How users experience your app

Android ships several **accessibility services**. Each one reads the same information from your UI, so getting the semantics right fixes things for all of them at once.

- **TalkBack** is the screen reader. Users swipe to move focus from element to element, TalkBack reads each one aloud, and a double tap activates it.
- **Select to Speak** reads out whatever the user taps or selects.
- **Switch Access** lets people navigate with one or more physical switches, a keyboard, or facial gestures through the front camera (Camera Switches) instead of touching the screen.
- **Voice Access** lets users control the device by speaking, for example "tap Send".
- **Font size, display size and high-contrast text** change how your layout renders, which is where hard-coded sizes break.
- **Magnification** lets users zoom into part of the screen with a triple tap or a shortcut.

The fastest way to understand all this is to turn on TalkBack and try to use your own app with your eyes closed. It's humbling the first time.

<img src="https://maikotrindade.com/public/img/mobile-accessibility.png" width="350" height="220" alt="A hand tapping a phone surrounded by icons for hearing, vision, mobility and touch accessibility"/>

## Semantics: what Compose tells accessibility services

Compose builds a **semantics tree** next to the UI tree. Each node describes what an element *means*: its text, its role (button, checkbox, heading), its state and the actions it supports. Accessibility services and UI tests both read this tree.

Components like `Text`, `Button`, `Checkbox` and `Switch` fill in their semantics automatically. Problems show up when you build custom components, use images, or compose small pieces into a bigger one. These are the fixes I use most.

### Describe images and icons

Give meaningful images a `contentDescription`. Pass `null` for decorative ones so TalkBack skips them instead of reading "unlabelled image".

```kotlin
Icon(
    imageVector = Icons.Default.Favorite,
    contentDescription = "Add to favourites"
)

Image(
    painter = painterResource(R.drawable.divider_wave),
    contentDescription = null // decorative
)
```

Don't include the role in the description ("button", "image"); TalkBack announces it already.

### Explain what a click does

By default TalkBack says "double tap to activate". A **click label** says what will actually happen:

```kotlin
Row(
    modifier = Modifier.clickable(
        onClickLabel = "Open article",
        onClick = { openArticle(article.id) }
    )
) {
    Text(article.title)
}
```

TalkBack now says "double tap to open article".

### Describe state

When a custom component has state, expose it. For anything that toggles, prefer `Modifier.toggleable`, which sets the state and role for you. For other states, set `stateDescription`:

```kotlin
Row(
    modifier = Modifier
        .toggleable(
            value = isSubscribed,
            role = Role.Switch,
            onValueChange = onSubscribedChange
        )
        .padding(16.dp)
) {
    Text("Weekly newsletter")
    Spacer(Modifier.weight(1f))
    Switch(checked = isSubscribed, onCheckedChange = null)
}
```

Setting `onCheckedChange = null` on the inner `Switch` matters: the whole row is the toggle, so the switch shouldn't be a separate focus stop.

### Merge related elements

A list item made of an avatar, a name, a timestamp and a preview can turn into four separate TalkBack stops. Users have to swipe four times per item, and the pieces lose their context. Merge them so the item is read as one:

```kotlin
Row(modifier = Modifier.semantics(mergeDescendants = true) {}) {
    Avatar(user)
    Column {
        Text(user.name)
        Text(message.preview)
    }
}
```

`Modifier.clickable` and `toggleable` merge their children automatically, which is another reason to put the click on the container rather than on a child.

### Mark headings

Screen reader users often jump between headings to skim a screen, the same way sighted users scan for bold text:

```kotlin
Text(
    text = "Recent orders",
    style = MaterialTheme.typography.titleLarge,
    modifier = Modifier.semantics { heading() }
)
```

## Visual and motor accessibility

Semantics covers screen readers and switches. These rules cover everyone else:

- **Touch targets of at least 48×48 dp.** Material components already enforce this. For custom clickable elements, add `Modifier.minimumInteractiveComponentSize()`.
- **Contrast of at least 4.5:1** for normal text and 3:1 for large text and meaningful icons (WCAG AA). Don't rely on colour alone to show errors or status; add an icon or text.
- **Use `sp` for text and let it grow.** Test at the largest font size. Text that's clipped or cut off with `maxLines = 1` is the most common bug I see.
- **Avoid gestures as the only way to do something.** Swipe-to-delete needs a visible alternative, because Switch Access and Voice Access users can't easily swipe.
- **Respect animation settings** for users who turn off animations.

## Testing accessibility

I test in three layers:

1. **Manually with TalkBack.** Nothing replaces moving through the real flow with a screen reader. Check the focus order, what gets read, and whether every action is reachable.
2. **With Accessibility Scanner.** Google's free app takes a screenshot and flags small touch targets, low contrast and missing labels.
3. **In automated UI tests.** Compose tests find nodes through the same semantics tree, so finding a node by its content description is itself an accessibility check:

```kotlin
@Test
fun favouriteButton_isAccessible() {
    composeTestRule.setContent { ArticleScreen(article) }

    composeTestRule
        .onNodeWithContentDescription("Add to favourites")
        .assertHasClickAction()
        .assertIsDisplayed()
}
```

If you can't find a button by its label in a test, TalkBack users can't identify it either. Recent versions of the Compose testing library can also run Google's Accessibility Test Framework checks automatically with `enableAccessibilityChecks()`, which catches contrast and touch-target issues as part of the normal test run.

## Where to start

If your app has never had an accessibility pass, don't try to fix everything at once. Turn on TalkBack, go through your most important flow (sign-in, checkout, the main screen) and fix what blocks you. Then add a label check to the tests for that flow so it stays fixed. If you're still moving screens from XML to Compose, make accessibility part of each migrated screen; my <a href="https://maikotrindade.com/2023/02/12/migration-from-jetpack-compose.html" target="_blank" rel="noopener" title="Migrating from XML views to Jetpack Compose">guide to migrating from XML to Compose</a> covers the rest of that process.

Android's <a href="https://developer.android.com/develop/ui/compose/accessibility" target="_blank" rel="noopener noreferrer" title="Accessibility in Jetpack Compose, Android Developers">Compose accessibility guide</a> covers the full semantics API, and the <a href="https://github.com/maikotrindade/InaccessibleApp" target="_blank" rel="noopener noreferrer" title="InaccessibleApp source on GitHub">InaccessibleApp repository</a> has the before-and-after examples from my talk.

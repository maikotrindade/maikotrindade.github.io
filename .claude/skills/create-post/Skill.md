---
name: create-post
description: >
  Creates a new Jekyll blog post for maikotrindade.github.io with correct filename,
  frontmatter, content structure, and checklist verification. Trigger with: "write a
  new blog post", "create a post about X", "draft a post on X", "new post about X",
  "add a blog post", "publish a post about X".
---

This skill produces a complete, publish-ready `_posts/YYYY-MM-DD-slug.markdown` file applying all site conventions: naming, frontmatter, content structure, and the post-creation checklist. At the end, it reminds you to update `llms.txt` and the `sitemap.xml`.

## Activation Triggers

- "Write a new blog post about Jetpack Compose state hoisting"
- "Create a post about my Capitol Trades Tracker app"
- "Draft a post on using Koog for AI agents"
- "New blog post: Android accessibility testing"
- "Add a blog post about Kotlin Coroutines"

## Instructions

### Filename

- Pattern: `YYYY-MM-DD-descriptive-slug.markdown` in `_posts/`
- Use today's date unless the user specifies otherwise
- Slug: all lowercase, hyphens only, 3–6 words
- Examples: `2025-10-02-understanding-ai-agents-concepts-architecture-tools.markdown`, `2026-01-18-introducing-capitol-trades-tracker.markdown`

### Required Frontmatter

```yaml
---
layout: post
title: "Title in Quotes"
date: YYYY-MM-DD
published: true
categories: [category1, category2]
tags: [tag1, tag2, tag3]
description: "SEO description — max 160 chars"
---
```

Category rules:
- Array syntax, **lowercase hyphenated values only** — spaces become `%20` in URLs (bad)
- Established patterns: `[android, kotlin]`, `[ai-agents, kotlin]`, `[blockchain, solidity]`, `[AI, agents, Claude, Anthropic]`

Description rules:
- Hard max **160 characters**
- Standalone sentence with 1–2 primary keywords
- Do NOT start with "In this post…", "This article…", or "Today we…"
- Good: `"Introduction to Koog, JetBrains' open-source agentic AI framework for building autonomous AI agents on the JVM."`

### Optional Frontmatter

```yaml
image: /public/img/filename.png   # OG/Twitter/JSON-LD image; defaults to android-dev.png
keywords: "word, word"            # Overrides tags for the keywords meta tag
```

### Content Structure

**Opening paragraph** — the excerpt. No heading before it. Must be standalone and descriptive (shown on blog index and used as SEO fallback).

**Headings:**
- `###` — main sections
- `####` — subsections
- Never `#` (H1) — the post layout already renders `page.title` as H1
- `##` is acceptable only for major top-level sections in very long posts

**Images** — inline HTML only (not Markdown `![]()` syntax):
```html
<img src="https://maikotrindade.com/public/img/filename.png" width="380" height="380" alt="description"/>
```
- Absolute URL required (`https://maikotrindade.com/…`)
- Canonical width: **380px** — adjust height proportionally
- Store images in `public/img/`

**Code blocks** — fenced with language identifier (Rouge syntax highlighting):
````
```kotlin
fun main() { println("Hello") }
```
````
Supported languages: `kotlin`, `java`, `solidity`, `javascript`, `swift`, `bash`, `yaml`, `html`, `css`, `json`

**Inline formatting:**
- `**bold**` — key terms on first introduction
- `*italic*` — emphasis or foreign terms
- `` `code` `` — function names, class names, code identifiers

**External links** — reference-style at bottom of file:
```markdown
See [official docs][kotlin-docs] for details.

[kotlin-docs]: https://kotlinlang.org/docs/
```

### Post-Creation Checklist

Run through every item before presenting the final file:

```
[ ] Filename: YYYY-MM-DD-slug.markdown in _posts/
[ ] layout: post
[ ] published: true (or false for draft)
[ ] title: in quotes
[ ] date: matches filename date
[ ] categories: array, lowercase hyphenated, no spaces
[ ] tags: array, specific terms
[ ] description: ≤160 chars, no "In this post…" opener, includes primary keywords
[ ] First paragraph is standalone excerpt (no heading above it)
[ ] No H1 (#) in body
[ ] Images: inline HTML, absolute URL (https://maikotrindade.com/…), width="380"
[ ] Code: fenced with language identifier
[ ] Update llms.txt if post is significant
```

### Updating `llms.txt`

`llms.txt` is **manually maintained** (unlike `sitemap.xml`/`atom.xml` which are Liquid-generated). After publishing a notable post, add one entry under the matching section:

```
- [Post Title](https://maikotrindade.com/category/YYYY/MM/DD/slug.html): One-sentence summary.
```

Sections in `llms.txt`: `## Blog — AI & Agents`, `## Blog — Android & Jetpack Compose`, `## Blog — Blockchain & Solidity`

### Template Reference

`_posts/base-post-format.markdown` — kept with `published: false`. Shows image syntax, link syntax, and inline formatting examples. **Never add a date to this file** — Jekyll would publish it.

---

## Example

A complete minimal post demonstrating all required elements:

**Filename:** `_posts/2026-05-03-kotlin-coroutines-flow-practical-guide.markdown`

```markdown
---
layout: post
title: "Kotlin Coroutines and Flow: A Practical Guide"
date: 2026-05-03
published: true
categories: [android, kotlin]
tags: [Kotlin, Coroutines, Flow, Android, Async]
description: "A practical guide to Kotlin Coroutines and Flow for managing asynchronous operations in Android apps."
---

Kotlin Coroutines and Flow have fundamentally changed how Android developers handle asynchronous programming. This guide covers the essentials you need to start using them confidently in production apps.

### Getting Started

Add the dependency to `build.gradle.kts`:

```kotlin
implementation("org.jetbrains.kotlinx:kotlinx-coroutines-android:1.7.3")
```

<img src="https://maikotrindade.com/public/img/coroutines-flow.png" width="380" height="240" alt="Coroutines and Flow diagram"/>

### Collecting a Flow

Use `collect` inside a `lifecycleScope` to safely observe state:

```kotlin
lifecycleScope.launch {
    viewModel.uiState.collect { state -> render(state) }
}
```

See the [official docs][coroutines-docs] for the complete API reference.

[coroutines-docs]: https://kotlinlang.org/docs/coroutines-overview.html
```

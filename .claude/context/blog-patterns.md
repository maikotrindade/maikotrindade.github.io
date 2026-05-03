# Blog Post Patterns

> Reference file for the `create-post` skill. The canonical checklist and rules live in `.claude/skills/create-post/Skill.md`.

## Frontmatter Schema (complete)

```yaml
---
layout: post                          # Always "post" — required
title: "Title With Quotes"            # Quoted string — required
date: YYYY-MM-DD                      # Publication date — required
published: true                       # Set false to draft — required
categories: [Category1, Category2]    # Array preferred; becomes URL path segments
tags: [tag1, tag2, tag3]              # Array; used for keywords meta and JSON-LD
description: "..."                    # Max 160 chars — MOST IMPORTANT SEO field — required
image: /public/img/filename.png       # Optional; OG/Twitter/JSON-LD image override
keywords: "word, word"                # Optional; overrides tags for keywords meta
---
```

## URL Structure

Jekyll generates URLs from date + category + slug:
`/category/YYYY/MM/DD/slug.html`

**Warning:** Categories with spaces become URL-encoded (`agentic%20systems` → bad). Prefer lowercase hyphenated single words.

Good: `categories: [ai-agents, kotlin]`
Bad: `categories: [AI agents, Agentic Systems]`

## File Naming

`YYYY-MM-DD-descriptive-slug.markdown` in `_posts/`

Examples:
```
2025-10-02-understanding-ai-agents-concepts-architecture-tools.markdown
2026-01-18-introducing-capitol-trades-tracker.markdown
2025-06-18-koog-ai-framework-agents.markdown
```

## Content Structure Patterns

### Opening paragraph
The first paragraph is the **excerpt** (shown on blog index, used as SEO fallback). It must be standalone and descriptive — no heading before it.

Good: `"AI agents are a paradigm shift in how we design and interact with artificial intelligence."`

### Headings
- `###` (H3) — main sections
- `####` (H4) — subsections
- Never use `#` (H1) in the body — the post layout renders `page.title` as H1
- `##` (H2) is acceptable for major top-level sections in very long posts

### Images
Use inline HTML (not Markdown `![]()` syntax):
```html
<img src="https://maikotrindade.com/public/img/filename.png" width="380" height="380" alt="description"/>
```
- Use **absolute URL** (`https://maikotrindade.com/...`), not root-relative
- Canonical width: **380px** — adjust height proportionally
- Store images in `public/img/`

### Code blocks
Fenced code with language identifier (Rouge syntax highlighting):
````
```kotlin
fun main() { println("Hello") }
```
````
Supported languages: `kotlin`, `java`, `solidity`, `javascript`, `swift`, `bash`, `yaml`, `html`, `css`, `json`

### Inline formatting
- `**bold**` — key terms on first introduction
- `*italic*` — emphasis or foreign terms
- `` `code` `` — function names, class names, code identifiers

### External links
Reference-style at bottom of file:
```markdown
[Link Text][ref-key]

[ref-key]: https://url.com
```

## Category Conventions (from existing posts)

| Topic | Category pattern |
|-------|-----------------|
| Android | `[android, compose, development]` or `[Android, Kotlin]` |
| AI/Agents | `[ai-agents, kotlin]` or `[artificial-intelligence]` |
| Blockchain | `[blockchain, solidity]` |
| Mixed | `[AI, Kotlin, Development, Agents]` |

Tags are more granular than categories.
- AI post tags: `[Koog, Kotlin, AI, Agents, JetBrains, JVM]`
- Android tags: `[Compose, Accessibility, Testing, Jetpack]`

## Description Field Rules

- Hard max: **160 characters**
- Standalone sentence summarizing the post
- Include 1–2 primary keywords naturally
- Do NOT start with "In this post…", "This article…", or "Today we…"

Good: `"Introduction to Koog, JetBrains' open-source agentic AI framework for building autonomous AI agents on the JVM."`

## New Post Checklist

```
[ ] Filename: YYYY-MM-DD-slug.markdown in _posts/
[ ] layout: post
[ ] published: true (or false for draft)
[ ] title: in quotes
[ ] date: matches filename date
[ ] categories: array, lowercase hyphenated values
[ ] tags: array, specific terms
[ ] description: ≤160 chars, no "In this post…" opener
[ ] First paragraph is standalone excerpt
[ ] No H1 (#) in body
[ ] Images: inline HTML, absolute URL, width="380"
[ ] Code: fenced with language identifier
[ ] Update llms.txt if post is significant
```

## Updating llms.txt

`llms.txt` is **manually maintained** (unlike `sitemap.xml` and `atom.xml` which are Liquid-generated).

After publishing a notable post, add an entry under the relevant section:
```
- [Post Title](https://maikotrindade.com/category/YYYY/MM/DD/slug.html): One-sentence summary.
```

Sections in `llms.txt`: `## Blog — AI & Agents`, `## Blog — Android & Jetpack Compose`, `## Blog — Blockchain & Solidity`

## Template Reference File

`_posts/base-post-format.markdown` — `published: false`, kept as a formatting starter. Shows image syntax, link syntax, inline formatting examples. Never add a date to this file (it would publish it).

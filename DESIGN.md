# Design

Canon direction, chosen by the user on 2026-11-05: a modern, clean, professional tech blog and dev portfolio. Craft bar: leerob.com and vercel.com/blog. Played straight: no gimmicks, no costume.

## Principles

- Monochrome first. Hierarchy comes from size, weight, and the neutral ramp, not color.
- One accent (blue) and only where it means "link in prose" or "focus".
- One column, one measure. Content is the interface; chrome is thin.
- Hairlines over boxes. Lists and rules instead of shadowed cards. Cards only where items are genuinely parallel and comparable (Projects).

## Type

- **Geist** (variable 400–600; 450 used for nav, list titles, chips) for everything; **Geist Mono** for code, dates, and numeric data only.
- Scale (rem at 16px root, 17px from 38rem): 0.8125 meta · 0.875 small · 1 body · 1.25 h3 · 1.5 h2 · 2.25 page/post title · clamp(2.25, 5vw, 3) home name.
- Headings weight 600, tracking -0.02em to -0.035em by size; body line-height 1.7; measure ≤ 68ch.

## Color tokens (`public/css/theme.css`)

| Token | Light | Dark |
| --- | --- | --- |
| `--bg` | `#ffffff` | `#0a0a0a` |
| `--bg-subtle` | `#fafafa` | `#111111` |
| `--bg-muted` | `#f2f2f2` | `#1a1a1a` |
| `--fg` | `#171717` | `#ededed` |
| `--fg-strong` | `#0a0a0a` | `#ffffff` |
| `--fg-muted` | `#5c5c5c` | `#a1a1a1` |
| `--fg-faint` | `#737373` | `#8f8f8f` |
| `--border` | `#ebebeb` | `#242424` |
| `--border-strong` | `#d4d4d4` | `#363636` |
| `--accent` | `#0062d1` | `#52a8ff` |

Light/dark follows the visitor's OS, with the manual toggle in the header (persisted in localStorage).

## Layout

- Container: 46rem max, 1.5rem side gutter (1rem under 30rem).
- Sticky header: avatar + name (home link) left, nav + theme toggle right; translucent background with backdrop blur and a hairline bottom border. Static (not sticky) under 40rem, with the nav as a scrollable second row.
- Footer: social icons (incl. RSS), preferred-source button, copyright, Privacy, Archive.
- Spacing rhythm: 0.25rem steps; sections separated by 4–5rem; more space above headings than below.

## Components

- **Buttons:** 2.5rem tall, radius 8px. Primary is solid `--fg-strong` with `--bg` text; secondary is bordered. No lift on hover; background/border shift only.
- **Post list rows:** title left, Mono date right (tabular), hairline separators; hover darkens the title and adds a faint underline.
- **Chips (tags, categories, skills):** radius 6px, `--bg-muted` fill, `--fg-muted` text, 0.8125rem.
- **Timeline (Experience, Education):** two-column grid, period in Mono on the left, role and description right; hairlines between entries; stacks on mobile.
- **Cards (Projects only):** 1px border, radius 12px, no shadow; hover darkens the border.
- **Code:** `--bg-subtle` block, 1px border, radius 8px; inline code in `--bg-muted`, no color tint.

## Motion

- 150ms ease-out on color, background, and border changes. No translate-on-hover, no entrance animations. Reduced motion respected.

## Don't

- Gradient text, glow, colored side borders, pill eyebrows above headings, emoji as UI icons, shadows as decoration.

# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Two audiences, weighted equally (confirmed 2026-11-05):

- **Hiring managers, recruiters, and potential collaborators** evaluating Maiko as a senior mobile engineer. They skim: who is this, how senior, what has he shipped, where is the résumé.
- **Engineers reading the blog**, usually arriving from search, social, or Google Discover on a single post about Android, Kotlin, Jetpack Compose, AI agents, or blockchain. They want the answer, code that reads well, and a reason to read the next post.

## Product Purpose

Personal site and technical blog of Maiko Trindade, Senior Mobile Engineer (14+ years in software, 10 in Android). It establishes professional credibility and publishes hands-on writing. Success: a visitor quickly understands seniority and focus, and readers stay for more than one post.

## Positioning

A working mobile engineer who writes from production experience across Android/Kotlin/Compose, React Native, on-device and agentic AI, and Solidity/blockchain, rather than a generalist content site.

## Operating Context

- Static Jekyll site on GitHub Pages; push to `master` deploys.
- ~75 posts, paginated blog index (5/page), archive, categories, tags.
- Static pages: Home, About, Experience, Projects (filter tabs), Education, Privacy.
- Ads only on posts of 300+ words (one 234x60 unit); AdSense script gated the same way.

## Capabilities and Constraints

- Vanilla JS only; no build step beyond Jekyll.
- Light and dark themes via `data-theme="dark"` with a manual toggle and localStorage persistence.
- Must not change: GA4/UA/AdSense IDs, `CNAME`, `ads.txt`, post URLs, SEO metadata behavior in `head.html`.
- Header nav is auto-generated from pages with `layout: page` / `page_no_ads`; Privacy is linked in the footer.

## Brand Commitments

- Name: Maiko Trindade. Handle: @maikotrindade.
- Headshot at `public/img/maiko-trindade.webp`.
- Social profiles: LinkedIn, GitHub, Devpost, Google Developer profile.
- Full visual redesign approved (2026-11-05). The user chose the conventional path: a modern, clean, professional tech blog and dev portfolio. Craft bar: leerob.com and vercel.com/blog.

## Evidence on Hand

- Résumé PDF: `public/maikotrindade.pdf`.
- Career timeline (`experience.html`), project portfolio (`projects.html`), education (`education.html`).
- Post images in `public/img/`.
- No testimonials, client logos, or metrics on hand; do not fabricate them.

## Product Principles

1. Credibility through specifics: real roles, shipped work, real posts; never vague claims.
2. Reading comes first on posts: code and prose legibility outrank decoration.
3. One identity across home, pages, and posts.
4. Fast and static: no heavy assets or frameworks on a reading site.

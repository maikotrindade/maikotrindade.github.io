# CLAUDE.md — maikotrindade.github.io

## Project Identity

Personal blog/portfolio for Maiko Trindade, Senior Mobile Engineer (14+ years, specializing in Android/Kotlin/Jetpack Compose/AI agents/Blockchain). Hosted at [maikotrindade.com](https://maikotrindade.com) via GitHub Pages. Topics: Android development, Jetpack Compose, Kotlin, AI agents, blockchain/Solidity.

## Tech Stack

- **Generator:** Jekyll (kramdown, Liquid templates, Rouge syntax highlighting)
- **Hosting:** GitHub Pages — push to `master` → auto-build
- **CSS:** Poole + Hyde framework + custom `theme.css` (dark mode via `data-theme="dark"` attribute)
- **JS:** Vanilla only — `theme-toggle.js` (light/dark toggle, localStorage persistence)
- **Fonts:** Google Fonts (PT Sans, Abril Fatface)
- **Analytics:** GA4 (`G-NPGMKKGTDM`) + legacy UA (`UA-66120129-1`) + AdSense (`ca-pub-4415452186185932`)

## Development Workflow

```bash
bundle exec jekyll serve   # local dev at localhost:4000 with live reload
bundle exec jekyll build   # build to _site/
git push origin master     # deploys to GitHub Pages automatically
```

**Never commit `_site/`** — it is the build output directory.

## File Structure

```
_posts/                  Blog posts: YYYY-MM-DD-slug.markdown
_layouts/                Five layouts (see Layout System below)
_includes/               head.html, sidebar.html, analytics.html
_config.yml              Jekyll config: url, author, pagination, exclude list
public/css/              poole.css, hyde.css, syntax.css, theme.css
public/js/               theme-toggle.js
public/img/              Profile photo, social icons, OG images, post images
blog/                    Blog index (paginated, 5/page) and archive
capitol-trades-tracker/  Standalone app showcase (en/, fr/ subdirs)
index.html               Home page (layout: default_no_ads)
about.html               About (layout: page_no_ads)
experience.html          Career timeline (layout: page_no_ads)
projects.html            Portfolio with filter tabs (layout: page_no_ads)
education.html           Education (layout: page_no_ads)
llms.txt                 Manually maintained blog index for LLM crawlers
robots.txt               Allows all AI crawlers (ClaudeBot, GPTBot, anthropic-ai…)
sitemap.xml, atom.xml    Liquid-generated; do not edit by hand
CNAME                    Custom domain — do not modify
ads.txt                  AdSense verification — do not modify
```

## Blog Post Conventions

See the `/create-post` skill (`.claude/skills/create-post/Skill.md`) for the complete post creation guide, frontmatter schema, content conventions, and checklist.

## Layout System

| Layout           | Has ads? | `head.html` included? | Used by                                |
| ---------------- | -------- | --------------------- | -------------------------------------- |
| `default`        | yes      | yes                   | blog/index.html                        |
| `default_no_ads` | no       | **no (inlined)**      | index.html (Home)                      |
| `post`           | yes      | yes (via default)     | all blog posts                         |
| `page`           | yes      | yes (via default)     | static pages (with ads)                |
| `page_no_ads`    | no       | **no (inlined)**      | about, experience, projects, education |

**Critical quirk:** `default_no_ads.html` does NOT use `{% include head.html %}`. It has its own hardcoded `<head>`. When editing SEO/meta behavior, check **both** `_includes/head.html` AND `_layouts/default_no_ads.html`.

**Sidebar auto-nav:** `sidebar.html` discovers nav items by filtering `site.pages` where `layout == "page"` or `layout == "page_no_ads"`. A new static page with the correct layout automatically appears in the sidebar — no changes to `sidebar.html` needed.

## Includes

| File                       | Purpose                                                                                  |
| -------------------------- | ---------------------------------------------------------------------------------------- |
| `_includes/head.html`      | Meta tags, OG, Twitter Cards, JSON-LD schema, GA4, AdSense, CSS links, `theme-toggle.js` |
| `_includes/sidebar.html`   | Profile photo, social links, auto-generated nav, last 3 posts                            |
| `_includes/analytics.html` | Legacy UA analytics (`UA-66120129-1`) — keep intact                                      |

### SEO metadata fallback chain (`head.html`)

- **description:** `page.description` → `page.excerpt` (strip HTML, truncate to 160) → `site.description`
- **image:** `page.image` → `https://maikotrindade.com/public/img/android-dev.png`
- **JSON-LD schema:** `layout == "post"` → Article schema; all other layouts → WebSite schema

## Critical Constraints

**Never modify:**

- GA4 ID: `G-NPGMKKGTDM` (in `head.html` and `default_no_ads.html`)
- AdSense ID: `ca-pub-4415452186185932` (in `head.html`)
- Legacy UA ID: `UA-66120129-1` (in `analytics.html`)
- `CNAME` file (controls custom domain)
- `ads.txt` (AdSense verification)

**Never commit `_site/`** — build output, not source.

## AI / LLM Files

- `llms.txt` — manually maintained blog index
- `robots.txt` — AI crawlers explicitly allowed; do not add Disallow rules for AI agents
- JSON-LD Article schema auto-injected on every `layout: post` page via `head.html`

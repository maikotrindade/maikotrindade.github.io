# Layouts and Includes Reference

## Layout Inheritance Tree

```
default_no_ads.html  (self-contained — does NOT use {% include head.html %})
  └── page_no_ads.html

default.html  (uses {% include head.html %}, {% include sidebar.html %}, {% include analytics.html %})
  ├── post.html
  └── page.html

blog/index.html  → layout: default (directly)
```

## Layout Decision Table

| Page type | Layout | Ads | `head.html` included |
|-----------|--------|-----|----------------------|
| Home (`index.html`) | `default_no_ads` | no | no (inlined head) |
| About, Projects, Education, Experience | `page_no_ads` | no | no (inlined head) |
| Blog index (`blog/index.html`) | `default` | yes | yes |
| All blog posts | `post` | yes | yes |
| New static page (no ads) | `page_no_ads` | no | no (inlined head) |
| New static page (with ads) | `page` | yes | yes |

## _includes/head.html

**Included by:** `default.html` (and thus `post.html`, `page.html`, `blog/index.html`)
**NOT included by:** `default_no_ads.html` — it has its own inlined `<head>` block

### What head.html injects

1. Charset, viewport, IE-compat meta
2. AdSense account meta: `ca-pub-4415452186185932`
3. Primary meta tags: title, description, author, keywords
4. Open Graph tags (`og:type = "article"` for posts, `"website"` otherwise)
   - For posts: `article:published_time`, `article:section`, `article:tag`
5. Twitter Card tags (`summary_large_image`)
6. Canonical link: `site.url + page.url`
7. GA4 gtag script: `G-NPGMKKGTDM`
8. AdSense script (`ca-pub-4415452186185932`)
9. `<title>` tag
10. CSS: `poole.css`, `syntax.css`, `hyde.css`, `theme.css`
11. Favicon + Apple touch icon
12. RSS/Atom feed link
13. JSON-LD structured data (see below)
14. `theme-toggle.js` script

### Metadata fallback chains

| Field | Fallback order |
|-------|---------------|
| `description` | `page.description` → `page.excerpt` (strip HTML, truncate 160) → `site.description` |
| `image` | `page.image` → `https://maikotrindade.com/public/img/android-dev.png` |
| `keywords` | `page.keywords` → `page.tags` joined → `page.categories` joined → hardcoded default |
| `title` | `page.title + " \| " + site.title` → `site.title` |

### JSON-LD schema logic

- `layout == "post"` → **Article** schema (headline, description, url, datePublished, dateModified, image, author, publisher, keywords)
- All other layouts → **WebSite** schema (name, url, author)

## _includes/analytics.html

Contains legacy Universal Analytics (`analytics.js`) with property `UA-66120129-1`. Included at the bottom of `<body>` in both `default.html` and `default_no_ads.html`. **Keep intact — do not remove or modify.** GA4 tracking runs in parallel via `head.html`.

## _includes/sidebar.html

### Profile section
- Links to `/`
- Profile image: `https://maikotrindade.com/public/img/maiko-trindade.webp` (140×140)
- `site.title` as `h2`
- Social icons: LinkedIn, GitHub, Devpost, Google Dev, Mastodon

### Auto-navigation (Liquid)
```liquid
{% for node in site.pages %}
  {% if node.title != null %}
  {% if node.layout == "page" or node.layout == "page_no_ads" %}
    <li><a href="{{ node.url }}">{{ node.title }}</a></li>
  {% endif %}
  {% endif %}
{% endfor %}
```

**Effect:** Any page file with `layout: page` or `layout: page_no_ads` AND a frontmatter `title` appears in the sidebar nav automatically. No edits to `sidebar.html` are needed when adding pages.

Order is determined by Jekyll's `site.pages` (filename-alphabetical by default). Home link is hardcoded above the loop.

### Latest Updates section
Shows 3 most recent posts via `site.posts | limit:3`. Links to `/blog` and `/blog/archive` are hardcoded.

## post.html layout

Wraps content in `<article>` with Schema.org microdata (`itemprop` attributes for BlogPosting). Renders: post title (H1), date, categories, tags (as spans), post content, author footer. After article: "Related Posts" section using `site.related_posts | limit:4`. Jekyll LSI is not configured, so related posts fall back to the 4 most recent posts.

## page.html and page_no_ads.html

Both render: `<div class="page"><h1 class="page-title">{{ page.title }}</h1>{{ content }}</div>`

Difference: `page_no_ads` uses `default_no_ads` as parent (no AdSense); `page` uses `default` (with AdSense).

## Adding a New Static Page

1. Create `filename.html` at project root (or in a subdirectory)
2. Add frontmatter:
   ```yaml
   ---
   layout: page_no_ads
   title: Page Title
   description: "SEO description"
   ---
   ```
3. Page automatically appears in sidebar nav
4. No changes needed to `sidebar.html` or `_config.yml`

## CSS Load Order

1. `poole.css` — base reset and typography (Poole framework)
2. `syntax.css` — Rouge syntax highlighting
3. `hyde.css` — sidebar layout and Hyde theme
4. `theme.css` — dark mode, custom components, overrides

Dark mode: `document.documentElement.setAttribute('data-theme', 'dark')`. All dark mode CSS overrides use `[data-theme="dark"]` selectors in `theme.css`.

## Theme Toggle (theme-toggle.js)

- Injects a `<button id="theme-toggle" class="theme-toggle">` into `<body>`
- Reads/writes `localStorage` key: `"theme-preference"`
- Falls back to `prefers-color-scheme: dark` if no stored preference
- Listens for system theme changes
- Runs before DOM ready (injected in `<head>`)

## Key _config.yml Settings

```yaml
url: https://maikotrindade.com      # Used in all absolute URL constructions
excerpt_separator: "\n\n"           # First paragraph = post excerpt
markdown: kramdown
highlighter: rouge
paginate: 5                         # Blog index: 5 posts per page
paginate_path: "/blog/page:num/"
include:
  - ads.txt                         # Force-include in build output
exclude:
  - README.md
  - LICENSE.md
  - Gemfile
  - Gemfile.lock
  - node_modules
  - vendor
```

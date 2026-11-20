#!/usr/bin/env python3
"""Create dev.to drafts for new Jekyll posts.

Each draft points its canonical URL back to maikotrindade.com, so the original
keeps the ranking credit. Drafts are never published: review them by hand.

Usage: crosspost.py [--dry-run] _posts/2026-01-01-slug.markdown [...]
Env:   DEVTO_API_KEY (optional; without it, nothing is posted).
"""
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request

import yaml

SITE_URL = "https://maikotrindade.com"
USER_AGENT = "jekyll-crosspost/1.0"


def parse_post(path):
    text = open(path, encoding="utf-8").read()
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", text, re.S)
    if not match:
        raise ValueError(f"{path}: no frontmatter")
    return yaml.safe_load(match.group(1)) or {}, match.group(2)


def as_list(value):
    if value is None:
        return []
    return value.split() if isinstance(value, str) else list(value)


def canonical_url(path, meta):
    # Jekyll's default "date" permalink: /:categories/:year/:month/:day/:title.html
    name = os.path.basename(path)
    match = re.match(r"(\d{4})-(\d{2})-(\d{2})-(.+)\.(markdown|md)$", name)
    if not match:
        raise ValueError(f"{path}: filename is not YYYY-MM-DD-slug.markdown")
    year, month, day, slug = match.group(1, 2, 3, 4)
    if meta.get("permalink"):
        return SITE_URL + meta["permalink"]
    categories = [str(c).lower() for c in as_list(meta.get("categories"))]
    parts = categories + [year, month, day, f"{slug}.html"]
    return f"{SITE_URL}/{'/'.join(parts)}"


def absolutize(markdown):
    # Site-relative links and images (/public/img/x.png) break off-site.
    markdown = re.sub(r"\]\((/[^)\s]*)", lambda m: f"]({SITE_URL}{m.group(1)}", markdown)
    return re.sub(r'(src|href)="(/[^"]*)"', lambda m: f'{m.group(1)}="{SITE_URL}{m.group(2)}"', markdown)


def image_url(meta):
    image = meta.get("image")
    if not image:
        return None
    return image if image.startswith("http") else SITE_URL + image


def footer(url):
    return f"\n\n---\n\n*Originally published at [maikotrindade.com]({url}).*\n"


def devto_tags(meta):
    # dev.to allows at most 4 tags, lowercase alphanumeric only.
    tags = []
    for tag in as_list(meta.get("tags")) + as_list(meta.get("categories")):
        clean = re.sub(r"[^a-z0-9]", "", str(tag).lower())
        if clean and clean not in tags:
            tags.append(clean)
    return tags[:4]


def request(url, payload, headers):
    data = json.dumps(payload).encode()
    req = urllib.request.Request(url, data=data, method="POST", headers={
        "Content-Type": "application/json", "User-Agent": USER_AGENT, **headers})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read() or b"{}")
    except urllib.error.HTTPError as err:
        raise RuntimeError(f"{url} -> HTTP {err.code}: {err.read().decode()[:500]}")


def wait_until_live(url, attempts=20, delay=30):
    # Pages deploys after this workflow starts; never point a canonical at a 404.
    for _ in range(attempts):
        try:
            req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=15) as resp:
                if resp.status == 200:
                    return True
        except urllib.error.URLError:
            pass
        time.sleep(delay)
    return False


def devto_draft(meta, body, url):
    article = {
        "title": meta["title"],
        "body_markdown": body,
        "published": False,
        "canonical_url": url,
        "tags": devto_tags(meta),
    }
    if meta.get("description"):
        article["description"] = meta["description"]
    if image_url(meta):
        article["main_image"] = image_url(meta)
    result = request("https://dev.to/api/articles", {"article": article}, {
        "api-key": os.environ["DEVTO_API_KEY"],
        "Accept": "application/vnd.forem.api-v1+json"})
    return result.get("url") or result.get("id")


def main(argv):
    dry_run = "--dry-run" in argv
    paths = [a for a in argv if a != "--dry-run"]
    platforms = []
    if os.environ.get("DEVTO_API_KEY"):
        platforms.append(("dev.to", devto_draft))
    if not platforms and not dry_run:
        print("No API secrets set; nothing to do.")
        return 0

    failed = False
    for path in paths:
        meta, content = parse_post(path)
        if meta.get("published") is False or meta.get("crosspost") is False:
            print(f"skip {path}: unpublished or crosspost: false")
            continue
        url = canonical_url(path, meta)
        body = absolutize(content.strip()) + footer(url)
        if dry_run:
            print(json.dumps({"post": path, "canonical": url, "devto_tags": devto_tags(meta),
                              "image": image_url(meta),
                              "body_chars": len(body)}, indent=2))
            continue
        if not wait_until_live(url):
            print(f"FAIL {path}: {url} never returned 200; no drafts created")
            failed = True
            continue
        for name, create in platforms:
            try:
                print(f"{name} draft for {path}: {create(meta, body, url)}")
            except Exception as err:  # report the failure and keep going with other posts
                print(f"FAIL {name} for {path}: {err}")
                failed = True
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

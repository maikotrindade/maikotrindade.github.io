#!/usr/bin/env python3
"""Tell IndexNow (Bing, Yandex, Seznam, Naver, Yep) which pages changed.

Google ignores IndexNow; it reads sitemap.xml through Search Console.
Send the full list only once. After that, pass only the URLs that changed.

Usage: indexnow.py              # every URL in the live sitemap.xml
       indexnow.py <url> [...]  # only these URLs
"""
import json
import sys
import urllib.error
import urllib.request

from indexnow_urls import batches, on_host, sitemap_urls

HOST = "maikotrindade.com"
KEY = "14b7422d297d698bea7e90c6ea969d3e"
KEY_LOCATION = f"https://{HOST}/{KEY}.txt"
ENDPOINT = "https://api.indexnow.org/indexnow"
BATCH = 10_000
USER_AGENT = "jekyll-indexnow/1.0"


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=30) as res:
        return res.read().decode("utf-8")


def main(args):
    if fetch(KEY_LOCATION).strip() != KEY:
        sys.exit(f"Key file at {KEY_LOCATION} does not match; deploy it first.")

    if args:
        urls = on_host(args, HOST)
    else:
        urls = on_host(sitemap_urls(fetch(f"https://{HOST}/sitemap.xml")), HOST)
    if not urls:
        sys.exit("No https URLs on this host to submit.")

    for batch in batches(urls, BATCH):
        body = json.dumps({"host": HOST, "key": KEY, "keyLocation": KEY_LOCATION, "urlList": batch}).encode()
        req = urllib.request.Request(
            ENDPOINT,
            data=body,
            headers={"Content-Type": "application/json; charset=utf-8", "User-Agent": USER_AGENT},
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as res:
                status = res.status
        except urllib.error.HTTPError as err:
            # 403 right after deploying the key: IndexNow cached the failed check. Retry in a few minutes.
            sys.exit(f"IndexNow HTTP {err.code}: {err.read().decode('utf-8', 'replace')}")
        print(f"Submitted {len(batch)} URLs: HTTP {status}.")


if __name__ == "__main__":
    main(sys.argv[1:])

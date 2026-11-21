"""Pure helpers for indexnow.py: no network, so they can be unit-tested."""
import re
from urllib.parse import urlparse


def sitemap_urls(xml):
    return re.findall(r"<loc>\s*(.*?)\s*</loc>", xml)


def on_host(urls, host):
    # IndexNow rejects the whole batch if any URL is on another host.
    return [u for u in dict.fromkeys(urls) if urlparse(u).scheme == "https" and urlparse(u).hostname == host]


def batches(urls, size):
    return [urls[start : start + size] for start in range(0, len(urls), size)]


STATUS_WORDS = {
    200: "accepted",
    202: "accepted, key check pending",
    400: "bad request (malformed JSON or URL)",
    403: "key not found or not valid (if the key file is live, retry in a few minutes)",
    422: "URLs or key do not match this host",
    429: "too many requests; wait before sending again",
}


def describe_status(code):
    return f"HTTP {code} {STATUS_WORDS.get(code, 'unexpected response')}"

"""Run: python3 -m unittest discover scripts"""
import unittest

from indexnow_urls import batches, on_host, sitemap_urls

HOST = "maikotrindade.com"


class SitemapUrlsTest(unittest.TestCase):
    def test_reads_every_loc_and_trims_whitespace(self):
        xml = "<urlset><url><loc>\n https://maikotrindade.com/a/ \n</loc></url><url><loc>https://maikotrindade.com/b/</loc></url></urlset>"
        self.assertEqual(sitemap_urls(xml), ["https://maikotrindade.com/a/", "https://maikotrindade.com/b/"])

    def test_empty_sitemap(self):
        self.assertEqual(sitemap_urls("<urlset></urlset>"), [])


class OnHostTest(unittest.TestCase):
    def test_keeps_only_https_on_exact_host(self):
        urls = [
            "https://maikotrindade.com/a/",
            "http://maikotrindade.com/b/",
            "https://www.maikotrindade.com/c/",
            "https://example.com/d/",
        ]
        self.assertEqual(on_host(urls, HOST), ["https://maikotrindade.com/a/"])

    def test_removes_duplicates_in_order(self):
        urls = ["https://maikotrindade.com/b/", "https://maikotrindade.com/a/", "https://maikotrindade.com/b/"]
        self.assertEqual(on_host(urls, HOST), ["https://maikotrindade.com/b/", "https://maikotrindade.com/a/"])


class BatchesTest(unittest.TestCase):
    def test_splits_into_chunks_of_size(self):
        self.assertEqual(batches(list(range(5)), 2), [[0, 1], [2, 3], [4]])

    def test_empty_list_has_no_batches(self):
        self.assertEqual(batches([], 10_000), [])


if __name__ == "__main__":
    unittest.main()

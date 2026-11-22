import unittest

from gfwlist import convert


class GFWListTests(unittest.TestCase):
    def test_scope_and_exception_order(self):
        rules = convert("""[AutoProxy 0.2.9]
||example.com
@@||safe.example.com
@@||*.tokenplus.app
www.example.net
|http://site.example/news
||cdn*.site.example
""").splitlines()
        self.assertEqual(rules[0], 'DOMAIN-SUFFIX,safe.example.com,DIRECT')
        self.assertIn('DOMAIN,www.example.net,PROXY', rules)
        wildcard, path, cdn = [line.split(',')[1] for line in rules if line.startswith('URL-REGEX,')]
        self.assertRegex('https://a.tokenplus.app/', wildcard)
        self.assertNotRegex('https://tokenplus.app/', wildcard)
        self.assertRegex('http://site.example/news/story', path)
        self.assertNotRegex('https://site.example/news', path)
        self.assertNotRegex('http://site.example/other', path)
        self.assertRegex('https://cdn01.site.example/file', cdn)
        self.assertNotRegex('https://cdn01.site.example.invalid/file', cdn)

    def test_unsupported_exception_fails_build(self):
        with self.assertRaises(ValueError):
            convert('[AutoProxy 0.2.9]\n||example.com\n@@||example.com$unsupported')


if __name__ == '__main__':
    unittest.main()

import unittest

from ad import extract_domains


class AdvertisingRuleTests(unittest.TestCase):
    def test_exception_order_does_not_change_result(self):
        block = '||ads.example^'
        exception = '@@||Ads.Example^'
        for rules in ([block, exception], [exception, block, block]):
            with self.subTest(rules=rules):
                self.assertEqual(extract_domains(rules), [])

    def test_exception_only_matches_complete_labels(self):
        rules = [
            '@@||example.example^',
            '||deep.ads.example.example^',
            '||ample.example^',
            '||notexample.example^',
            '||example.example.net^',
        ]
        self.assertEqual(extract_domains(rules), [
            'ample.example', 'example.example.net', 'notexample.example',
        ])

    def test_block_must_not_cover_an_excepted_child(self):
        rules = [
            '||example.org^', '||safe.example.org^', '||cdn.safe.example.org^',
            '||ads.example.org^', '@@||safe.example.org^',
        ]
        self.assertEqual(extract_domains(rules), ['ads.example.org'])

    def test_conditional_exceptions_do_not_allow_entire_hosts(self):
        for exception in (
            '@@||ads.example/banner.js',
            '@@||ads.example^$image,domain=publisher.example',
            '@@||cdn.example/path/ads.example',
            '@@||ads.example:443^',
            '@@|https://ads.example/',
            '@@/ads\\.example/',
        ):
            with self.subTest(exception=exception):
                self.assertEqual(extract_domains([
                    '||ads.example^', '||publisher.example^', exception,
                ]), ['ads.example', 'publisher.example'])

    def test_simple_exception_forms_and_ipv4_literals(self):
        for exception in ('@@ads.example', '@@||ads.example/*', '@@||*.ads.example^'):
            with self.subTest(exception=exception):
                self.assertEqual(extract_domains(['||a.ads.example^', exception]), [])
        self.assertEqual(extract_domains([
            '||192.0.2.10^', '||192.0.2.100^', '@@||192.0.2.10^',
        ]), ['192.0.2.100'])

    def test_existing_block_forms_local_exclusions_and_sorting(self):
        rules = [
            '! comment', '*', '[Adblock Plus 2.0]', '||z.example^', '|https://A.Example/*',
            'a.example', '||a.example^', '||b.example:443^', '||c.example/path',
            '||option.example^$script', 'hidden.example##.ad', '||child.z.example^',
        ]
        self.assertEqual(extract_domains(rules, ['z.example']), [
            'a.example', 'b.example', 'child.z.example',
        ])


if __name__ == '__main__':
    unittest.main()

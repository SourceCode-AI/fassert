import re
import unittest

from fassert import fassert


class MatchingPrimitivesTest(unittest.TestCase):
    def test_matching_primitives(self):
        test_data = (
            ("", ""),
            ("test_string", "test_string"),
            (b"test_bytes", b"test_bytes"),
            ("", re.compile(r"^$")),
            ("test", re.compile("[a-z]{4}")),
            (42, 42),
            (0, 0),
            (42.0, 42.0),
            (0.0, 0.0),
            (3.14, 3.14),
            (None, None),
            ((), ()),
            ([], []),
            (set(), set()),
            (dict(), dict()),
        )

        for data, template in test_data:
            with self.subTest(data=data, template=template):
                assert fassert(data, template)

    def test_same_type_different_value_not_matching(self):
        test_data = (
            ("", "value"),
            ("value", ""),
            (b"", b"value"),
            (0, 42),
            (42, 0),
            (1, 3),
            (42.0, 0.0),
            (0.0, 42.0),
        )

        for data, template in test_data:
            with self.subTest(data=data, template=template):
                self.assertRaises(AssertionError, fassert, data, template)


    def test_different_types_not_matching(self):
        test_data = (
            ("", ()),
            ("", []),
            ("", set()),
            (b"value", ""),
        )

        for data, template in test_data:
            with self.subTest(data=data, template=template):
                self.assertRaises(AssertionError, fassert, data, template)

            with self.subTest(data=template, template=data):
                self.assertRaises(AssertionError, fassert, template, data)

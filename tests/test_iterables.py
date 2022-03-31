import unittest

from fassert import fassert


class IterablesTest(unittest.TestCase):
    def test_exact_list(self):
        test_data = (
            [],
            ["a"],
            [42],
            ["a", 42, None],
            (),
            ("a",),
            (42),
            ("a", "42", None),
            set(),
            {"a"},
            {"a", 42, None},
        )
        for data in test_data:
            with self.subTest(data=data):
                self.assertIs(fassert(data, data), True)

    def test_subtest(self):
        test_data = (
            (["a", "b"], ["a"]),
            (("a", "b"), ("a",)),
            # TODO: ({"b", "a"}, {"a"})
        )
        for data, template in test_data:
            with self.subTest(data=data, template=template):
                self.assertIs(fassert(data, template), True)

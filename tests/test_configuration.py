import unittest
import re

from fassert import FuzzyAssert


class ConfigurationTest(unittest.TestCase):
    def test_eval_function(self):
        data = "test"
        template = lambda x: len(x) == 4

        fasserter = FuzzyAssert()

        self.assertIs(fasserter.eval_functions, True)
        fasserter.match(data, template)

        fasserter.eval_functions = False
        self.assertRaises(AssertionError, fasserter.match, data, template)

    def test_fuzzy_sequence_types(self):
        test_data = (
            ((), []),
            (set(), ()),
            (set(), []),
        )

        fasserter = FuzzyAssert()
        self.assertIs(fasserter.fuzzy_sequence_types, False)

        for data, template in test_data:
            with self.subTest(data=data, template=template):
                self.assertRaises(AssertionError, fasserter.match, data, template)

            with self.subTest(data=template, template=data):
                self.assertRaises(AssertionError, fasserter.match, template, data)

    def test_check_minimum_sequence_length(self):
        test_data = (
            ([""], ["", ""]),
            (["test"], [re.compile(".{4}"), "test", re.compile("^test$")])
        )

        fasserter = FuzzyAssert()


        for data, template in test_data:
            with self.subTest(data=data, template=template):
                fasserter.check_minimum_sequence_length = True
                self.assertRaises(AssertionError, fasserter.match, data, template)

                fasserter.check_minimum_sequence_length = False
                self.assertIs(fasserter.match(data, template), True)


    def test_regex_allowed(self):
        test_data = (
            ("", re.compile("")),
            ("test", re.compile("^test$")),
            ("test", re.compile("test")),
            ("test", re.compile(".{4}"))
        )

        fasserter = FuzzyAssert()

        for data, template in test_data:
            with self.subTest(data=data, template=template):
                fasserter.regex_allowed = False
                self.assertRaises(AssertionError, fasserter.match, data, template)

                fasserter.regex_allowed = True
                self.assertIs(fasserter.match(data, template), True)

            with self.subTest(data=template, template=data):
                fasserter.regex_allowed = True
                # a string would never match regex, e.g. the regex matches are one way only from template to data
                self.assertRaises(AssertionError, fasserter.match, template, data)

import re
import unittest


class ReadmeTest(unittest.TestCase):
    # Copy-paste the example code from README into this test
    def test_readme_main_example(self):
        from fassert import fassert


        # Usage: fassert(<data>, <template>)

        fassert("This is expected", "This is expected")

        fassert("This matches as well", re.compile(r"[thismachewl ]+", re.I))

        fassert(
            {"key": "value", "key2": "value2"},
            {"key": "value"}
        )  # key2: value2 is ignored as it's not defined in the template

        fassert(
            {"key": "value", "abc": "value"},
            # You can nest and combine the fuzzy matching types in containers
            {re.compile(r"[a-z]{3}"): "value"}
        )

        fassert(
            [1, {"very": {"nested": {"dictionary": "data"}}}, {"not": "this"}],
            # Isn't this cool?
            [{"very": {re.compile(".{6}"): {"dictionary": lambda x: len(x) == 4}}}]
        )

        # Template can contain callables as well
        fassert("value", lambda x: x == "value")

        try:
            fassert("expected", "to not match")
            fassert({"a": "b"}, {"c": "d"})  # This will fail, {"c":"d"} is not in the target data
            fassert([1, 2, 3], [4])
            fassert("string", b"string")  # bytes != string in fassert
        except AssertionError:
            pass  # All the examples within the try block above will raise this exception

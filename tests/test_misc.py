import re
import unittest


class ReadmeTest(unittest.TestCase):
    # Copy-paste the example code from README into this test
    def test_readme_main_example(self):
        from fassert import fassert


        # Usage: fassert(<data>, <template>)

        fassert("This is expected", "This is expected")

        fassert("This matches as well", re.compile(r"[thismacewl ]+", re.I))

        fassert(
            {"key": "value", "key2": "value2"},
            {"key": "value"}
        )  # key2: value2 is ignored as it's not defined in the template

        fassert(
            {"key": "value"},
            # You can nest and combine the fuzzy matching types in containers
            {re.compile(r"[a-z]{3}"): "value"}
        )

        # Template can contain callables as well
        fassert("value", lambda x: x == "value")

        try:
            fassert({"a": "b"}, {"c": "d"})  # This will fail, {"c":"d"} is not in the target data
        except AssertionError:
            pass  # All the examples within the try block above will raise this exception

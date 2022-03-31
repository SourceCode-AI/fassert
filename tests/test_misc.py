import re
import unittest
from typing import Literal, Any


class ReadmeTest(unittest.TestCase):
    # Copy-paste the example code from README into this test
    def test_readme_main_example(self):
        from fassert import fassert

        # Usage: fassert(<data>, <template>)

        fassert("This is expected", "This is expected")

        fassert("This matches as well", re.compile(r"[thismachewl ]+", re.I))

        fassert(
            {"key": "value", "key2": "value2"}, {"key": "value"}
        )  # key2: value2 is ignored as it's not defined in the template

        fassert(
            {"key": "value", "abc": "value"},
            # You can nest and combine the fuzzy matching types in containers
            {re.compile(r"[a-z]{3}"): "value"},
        )

        fassert(
            [1, {"very": {"nested": {"dictionary": "data"}}}, {"not": "this"}],
            # Isn't this cool?
            [{"very": {re.compile(".{6}"): {"dictionary": lambda x: len(x) == 4}}}],
        )

        # Template can contain callables as well
        fassert("value", lambda x: x == "value")

        try:
            fassert("expected", "to not match")
            fassert(
                {"a": "b"}, {"c": "d"}
            )  # This will fail, {"c":"d"} is not in the target data
            fassert([1, 2, 3], [4])
            fassert("string", b"string")  # bytes != string in fassert
        except AssertionError:
            pass
        else:
            raise RuntimeError(
                "All examples within the try block must raise the AssertionError"
            )

    # Copy paste the custom type example in the advanced usage section over here
    def test_advanced_custom_type_example(self):
        from fassert import fassert, FassertInterface, FuzzyAssert

        class IsNumberEvenOrEqual(FassertInterface):
            def __init__(self, value):
                self.value = value

            def __fassert__(
                self, other: Any, matcher: FuzzyAssert, as_template: bool
            ) -> Literal[True]:
                if self.value == other:
                    return True
                elif isinstance(other, (int, float)) and int(other) % 2 == 0:
                    return True

                raise AssertionError("Data does not match the template")

        # In these examples the parameter `as_template` would be set to True as the data type is used as a template for matching
        fassert(10, IsNumberEvenOrEqual(15))
        fassert(15, IsNumberEvenOrEqual(15))
        fassert(42.0, IsNumberEvenOrEqual(15))

        try:
            fassert(15, IsNumberEvenOrEqual(17))
            fassert("some_string", IsNumberEvenOrEqual(15))
        except AssertionError:
            pass
        else:
            raise RuntimeError(
                "All examples within the try block must raise the AssertionError"
            )

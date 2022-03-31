import unittest

from fassert import fassert, FuzzyAssert, FassertInterface


class ByteStringMatcher(FassertInterface):
    def __init__(self, value):
        self.value = value

    def __fassert__(self, other, matcher, as_template):
        if isinstance(self.value, bytes) and isinstance(other, str):
            if self.value == other.encode():
                return True
        elif isinstance(self.value, str) and isinstance(other, bytes):
            if self.value.encode() == other:
                return True
        elif self.value == other:
            return True

        raise AssertionError("Data does not match the template")

    def __repr__(self):
        return f"<ByteStringMatcher({repr(self.value)})>"


class CheckIsTemplate(FassertInterface):
    def __fassert__(self, other, matcher, as_template):
        if as_template is not True:
            raise AssertionError("This must be matched as template")
        return True


class CustomTypesTest(unittest.TestCase):
    def test_byte_string_matcher(self):
        test_data = (
            (b"test", "test"),
            (b"", ""),
        )

        for data, template in test_data:
            with self.subTest(data=data, template=template):
                # Normally these types would not match
                self.assertRaises(AssertionError, fassert, data, template)
                # Our custom interface fuzzy matches the bytes to string
                self.assertIs(fassert(ByteStringMatcher(data), template), True)

            with self.subTest(data=template, template=data):
                self.assertRaises(AssertionError, fassert, template, data)
                self.assertIs(fassert(ByteStringMatcher(template), data), True)

    def test_check_is_template(self):
        checker = CheckIsTemplate()

        for data in ("", [], {}, 42, b"test", set()):
            with self.subTest(data=data):
                self.assertIs(fassert(data, checker), True)
                self.assertRaises(AssertionError, fassert, checker, data)

import inspect
from abc import ABC, abstractmethod
from typing import Pattern, Sequence, Literal, Any

__version__ = "0.3"


class FuzzyAssert:
    def __init__(self):
        self.eval_functions = True
        self.regex_allowed = True
        self.check_minimum_sequence_length = True
        self.fuzzy_sequence_types = False

    def match(self, data: Any, template: Any) -> Literal[True]:
        """
        Attempt to match the template onto the data.
        Each item in a `template` must have a match in the `data`.
        Extra items/data inside the `data` (if it is a container type) is ignored.

        :param data: Data to match against, extra data, container types or other python types is ignored
        :param template: Template to match against, everything defined here must have a match
        :raises AssertionError: Raised when data does not match the given template
        :return: True if `template` matches the `data`
        :rtype: Literal[True]
        """
        if isinstance(template, FassertInterface):
            return template.__fassert__(other=data, matcher=self, as_template=True)
        elif isinstance(data, FassertInterface):
            return data.__fassert__(other=template, matcher=self, as_template=False)

        elif inspect.isfunction(template):
            if self.eval_functions and template(data):
                return True
            raise AssertionError("Template function does not match the data")
        elif self.regex_allowed and type(data) == str and isinstance(template, Pattern):
            if not template.match(data):
                raise AssertionError(
                    "Template regex `{}` does not match the data".format(repr(template))
                )
            else:
                return True
        # This must be before generic test of Sequence types because str/bytes are also considered as sequences
        elif isinstance(data, (str, bytes)) and isinstance(template, (str, bytes)):
            if data == template:
                return True
            else:
                raise AssertionError("Template does not match the data")
        elif (
            isinstance(data, Sequence)
            and isinstance(template, Sequence)
            and (self.fuzzy_sequence_types or (type(data) == type(template)))
        ):
            if self.check_minimum_sequence_length and len(template) > len(data):
                raise AssertionError(
                    "Template sequence length is higher then the length of the data: `{}`".format(
                        template
                    )
                )
            elif len(template) == 0:
                return True

            for template_item in template:
                for data_item in data:
                    try:
                        self.match(data_item, template_item)
                        break
                    except AssertionError:
                        continue
                else:
                    raise AssertionError(
                        "Sequence item from the `template` not found inside the `data`: `{}`".format(
                            template_item
                        )
                    )
            return True

        if type(data) != type(template):
            raise AssertionError(
                f"Template type `{type(template)}` does not match the type of data `{type(data)}`"
            )
        elif isinstance(data, dict):
            for template_key, template_value in template.items():
                for data_key, data_value in data.items():
                    try:
                        self.match(data_key, template_key)
                        self.match(data_value, template_value)
                        break
                    except AssertionError:
                        continue
                else:
                    raise AssertionError(
                        "Could not find a matching key/value for dictionary item `{}`:`{}`".format(
                            repr(template_key), repr(template_value)
                        )
                    )
            return True
        else:
            if data == template:
                return True
            else:
                raise AssertionError(
                    "Target data does not match the template: `{}`".format(
                        repr(template)
                    )
                )


class FassertInterface(ABC):
    @abstractmethod
    def __fassert__(
        self, other: Any, matcher: FuzzyAssert, as_template: bool
    ) -> Literal[True]:
        """
        Add a support for matching custom defined types in a recursive way

        :param other: other data structure to match against
        :param matcher: An instance of the FuzzyAssert object
        :param as_template: Flag to indicate if you are (self) the template matching the data or the other way around
        :raises AssertionError: When `self` does not match the `other`
        :return: True if data is matching otherwise an AssertionError is raised
        :rtype Literal[True]:
        """
        ...


def fassert(data: Any, template: Any) -> Literal[True]:
    return FuzzyAssert().match(data, template)

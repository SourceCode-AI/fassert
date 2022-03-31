[![PyPI version](https://badge.fury.io/py/fassert.svg)](https://badge.fury.io/py/fassert)
![No dependencies](https://img.shields.io/badge/ZERO-Dependencies-blue)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

^fassert$: Fuzzy assert
---------------------

Fuzzy assert in your tests only a subset of data that matters

```
from fassert import fassert

# Usage: fassert(<data>, <template>)

fassert("This is expected", "This is expected")

fassert("This matches as well", re.compile(r"[thismachewl ]+", re.I))

fassert(
    {"key": "value", "key2": "value2"},
    {"key": "value"}
) # key2: value2 is ignored as it's not defined in the template

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
    pass
else:
    raise RuntimeError("All examples within the try block must raise the AssertionError")
```

In fassert, you can define a template to match your data against.
When you use a type that is a container (e.g. list, tuple, dict, etc...), then only the data that you defined in the template will be asserted.
All the addition data in the container will be ignored

Did you know this project is also dedicated to have **0 dependencies** on other packages?

Installation
------------

From PyPI:
`pip install fassert`

Locally:
```
pip install . 

# Run tests with:
python -m unittest discover -s tests/
```



Advanced usage
--------------

`fassert` function is equivalent in creating a default `FuzzyAssert()` object and calling match on it.
You can configure some behaviour of the fuzzy matcher via the object attributes like so:

```
from fassert import FuzzyAssert

fasserter = FuzzyAssert()
# Eval functions is turned on by default
fasserter.match("value", lambda x: x == "value")

fasserter.eval_functions = False
# This will now raise Assertion error
fasserter.match("value", lambda x: x == "value")

```

Bellow is an overview of the configurable options and their default values

| Name                          | Default value | Description                                                                            |
|-------------------------------|---------------|----------------------------------------------------------------------------------------|
| eval_functions                | True          | Enable template matching as callable functions                                         |
| regex_allowed                 | True          | Enable matching regexes from template agains strings in the data                       |
| fuzzy_sequence_types          | False         | Ignore types of similar sequence types when matching the template (e.g. tuple vs list) |
| check_minimum_sequence_length | True          | Check that the data has a minimum length of greater or equal to the template           |


You can also define custom data types such as following:

```
from fassert import fassert, FassertInterface, FuzzyAssert

class IsNumberEvenOrEqual(FassertInterface):
    def __init__(self, value):
        self.value = value

    def __fassert__(self, other: Any, matcher: FuzzyAssert, as_template: bool) -> Literal[True]:
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
    raise RuntimeError("All examples within the try block must raise the AssertionError")
```

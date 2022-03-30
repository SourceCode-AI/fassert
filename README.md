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
    pass  # All the examples within the try block above will raise this exception
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

fassert: Fuzzy assert
---------------------

Assert in your tests only a subset of data that matters

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
```

In fassert, you can define a template to match your data against.
When you use a type that is a container (e.g. list, tuple, dict, etc...), then only the data that you defined in the template will be asserted.
All the addition data in the container will be ignored

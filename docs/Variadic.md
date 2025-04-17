## Variadic.

#### Variadic types is:

- **list**

- **tuple**

- **set** and **frozenset**

- **collections.deque**

### Base usage:

```python
class Temp(BaseModel):
    # A keyword argument can take any number of values unless otherwise specified.
    a: list = pa.KwArg(description="This is required keyword variadic argument")

    # A keyword argument can accept exactly the specified number of values.
    b: list = pa.KwArg(description="This is required keyword variadic argument", n_args=3)

    # A keyword argument can accept the number of values specified in the range
    # From 2 to 4 values inclusive.
    c: list = pa.KwArg(description="This is required keyword variadic argument", n_args="2...4")
    # No more than 4 values inclusive
    d: list = pa.KwArg(description="This is required keyword variadic argument", n_args="...4")
    # At least 2 values
    e: list = pa.KwArg(description="This is required keyword variadic argument", n_args="2...")

    # Can be optional
    f: list = pa.KwArg([1, 2, 3], description="This is optional keyword variadic argument")
    g: list = pa.KwArg(None, description="This is optional keyword variadic argument")
```

### Advanced usage:

```python
from pydantic import BaseModel
import pydantic_argparse_next as pa
from pathlib import Path


class Temp(BaseModel):
    # Pydantic may attempt to cast values to the specified type.
    # For all variadic types except tuple, only the first specified type is considered.
    a: list[int] = pa.KwArg(description="This is required keyword variadic argument")

    # For a tuple containing other types inside itself
    # Each individual value will be converted to each individual type in the order they are specified.
    # Also in this case the number of expected values will strictly correspond to the number of types specified inside.
    # The n_args parameter will be ignored.
    b: tuple[int, str, Path] = pa.KwArg(description="This is required keyword variadic argument")


cliargs = pa.parse(Temp, program_name="Example program", description="The example program description")

print(cliargs)
```

Input:

```bash
appname --a "1" 2 "3"" --b "1" "two" "C:/example/three.json"
```

Output:

```
a=[1, 2, 3] b=(1, 'two', WindowsPath('C:/example/three.json'))
```

### Positional arguments:

```python
from pydantic import BaseModel
import pydantic_argparse_next as pa


class Temp(BaseModel):
    # For positional arguments, the number of values must be specified exactly.
    a: list = pa.Arg(description="This is required positional argument", n_args=3)
    b: tuple[int, int, int] = pa.Arg(description="This is optional positional argument")


cliargs = pa.parse(Temp, program_name="Example program", description="The example program description")

print(cliargs)
```

Input:

```bash
appname 1 2 3 1 2 3
```

Output:

```
a=['1', '2', '3'] b=(1, 2, 3)
```

## Store True \ False

## Example 1:

```python
from pydantic import BaseModel
import pydantic_argparse_new as pa


class Temp(BaseModel):
    a: bool = pa.KwArg(False, description="This is store true keyword argument")
    b: bool = pa.KwArg(True, description="This is store false keyword argument")


cliargs = pa.parse(Temp)

print(cliargs)
```

Input:

```bash
appname --a "choice2"
```

Output:

```
a=<Choices.choice2: 2> b=<Choices.choice1: 1> c=None
```

Help:

<img title="" src="./imgs/Advanced/StoreTrueFalse/example1.png" alt="img" width="800">

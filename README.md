# pydantic-argparse-next

Argument parser based on pydantic v2.

### Install:

```bash
pip install pydantic-argparse-next
```

### Base usage:

# 

```python
from pydantic import BaseModel, Field
import pydantic_argparse_next as pa


class Temp(BaseModel):
    # Positional arguments
    a: str = pa.Arg(description="This is a required positional argument.")
    b: str = pa.Arg("defalut_value", description="This is a OPTIONAL positional argument.")

    # Keyword arguments
    # Simple attributes or pydantic.Field are keyword arguments.
    c: str
    d: str = Field(None, description="This is a OPTIONAL keyword argument.")
    e: str = pa.KwArg(description="This is a required keyword argument.")
```

```
Input: appname "test1" --c "test2" --e="test3"
Output: a='test1' b='defalut_value' c='test2' d=None e='test3'
```

 **More details in the documentation**

### Supports:

✅ Positional arguments

        ✅ Required positional arguments

        ✅ Optional positional arguments

✅ Keyword arguments

        ✅ Required keyword arguments

        ✅ Optional keyword arguments

✅ Subcommands

        ✅ Required subcommands

        ✅ Optional subcommands

        ✅ Subcommands within subcommands

✅ Actions

        ✅ Choice (And simple text and Enum object)

        ✅ Store True

        ✅ Store False

        ✅ Variadic arguments

⬜ Extra

        ⬜ Easy saving config to file

        ⬜ Easy load config from file

**More details in the documentation**

### Docs and examples:

1. [Base usage](https://github.com/overgodofchaos/pydantic-argparse-next/blob/main/docs/BaseUsage.md)

2. Actions
   
   1. [Choice](https://github.com/overgodofchaos/pydantic-argparse-next/blob/main/docs/Choice.md)
   
   2. [Store True and Store False](https://github.com/overgodofchaos/pydantic-argparse-next/blob/main/docs/StoreTrueFalse.md)
   
   3. [Subcommands](https://github.com/overgodofchaos/pydantic-argparse-next/blob/main/docs/Subcommands.md)
   
   4. [Variadic](https://github.com/overgodofchaos/pydantic-argparse-next/blob/main/docs/Variadic.md)

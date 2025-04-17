from pydantic import BaseModel
import pydantic_argparse_next as pa


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


cliargs = pa.parse(Temp, program_name="Example program", description="The example program description")

print(cliargs)

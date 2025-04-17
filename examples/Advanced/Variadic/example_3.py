from pydantic import BaseModel
import pydantic_argparse_next as pa


class Temp(BaseModel):
    # For positional arguments, the number of values must be specified exactly.
    a: list = pa.Arg(description="This is required positional argument", n_args=3)
    b: tuple[int, int, int] = pa.Arg(description="This is optional positional argument")


cliargs = pa.parse(Temp, program_name="Example program", description="The example program description")

print(cliargs)


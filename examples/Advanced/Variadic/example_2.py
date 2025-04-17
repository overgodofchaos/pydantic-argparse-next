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


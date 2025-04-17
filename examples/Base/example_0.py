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


cliargs = pa.parse(Temp, program_name="Example program", description="The example program description")

print(cliargs)

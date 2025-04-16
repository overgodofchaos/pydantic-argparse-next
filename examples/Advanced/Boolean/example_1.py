from pydantic import BaseModel
import pydantic_argparse_next as pa


class Temp(BaseModel):
    # Store True\False arguments can't be positional
    a: bool = pa.KwArg(False, description="This is store true keyword argument")
    b: bool = pa.KwArg(True, description="This is store false keyword argument")


cliargs = pa.parse(Temp, program_name="Example program", description="The example program description")

print(cliargs)
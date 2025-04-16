from pydantic import BaseModel
from typing import Optional
import pydantic_argparse_new as pa


class Temp(BaseModel):
    a: str  # This is required keyword argument
    b: str | None  # This is optional keyword argument
    c: Optional[str]  # This is optional keyword argument


cliargs = pa.parse(Temp, program_name="Example program", description="The example program description")

print(cliargs)

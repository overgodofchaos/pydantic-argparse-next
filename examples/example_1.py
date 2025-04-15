from pydantic import BaseModel
from typing import Optional
from pydantic_argparse_new import parse


class Temp(BaseModel):
    a: str  # This is required keyword argument
    b: str | None  # This is optional keyword argument
    c: Optional[str]  # This is optional keyword argument


cliargs = parse(Temp, program_name="Example program", description="The example program description")

print(cliargs)

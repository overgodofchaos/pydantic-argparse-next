from pydantic import BaseModel
from typing import Literal
import pydantic_argparse_new as pa


class Temp(BaseModel):
    a: Literal["choice1", "choice2"] = pa.KwArg(..., description="This is a required keyword choice argument")
    b: Literal["choice1", "choice2"] = pa.KwArg("choice1", description="This is a optional keyword choice argument")
    c: Literal["choice1", "choice2"] = pa.KwArg(None, description="This is a optional keyword choice argument")


cliargs = pa.parse(Temp, program_name="Example program", description="The example program description")

print(cliargs)

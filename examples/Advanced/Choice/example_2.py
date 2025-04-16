from pydantic import BaseModel
from enum import Enum
import pydantic_argparse_new as pa


class Choices(Enum):
    choice1 = 1
    choice2 = 2


class Temp(BaseModel):
    a: Choices = pa.KwArg(..., description="This is a required keyword choice argument")
    b: Choices = pa.KwArg(Choices.choice1, description="This is a optional keyword choice argument")
    c: Choices = pa.KwArg(None, description="This is a optional keyword choice argument")


cliargs = pa.parse(Temp, program_name="Example program", description="The example program description")

print(cliargs)

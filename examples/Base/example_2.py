from pydantic import BaseModel, Field
from typing import Optional
import pydantic_argparse_new as pa
from pathlib import Path


class Temp(BaseModel):
    a: str = Field()  # This is a required keyword argument
    b: str = Field(..., description="This is a required keyword argument")
    c: str | None = Field(description="This is a optional keyword argument")
    d: Optional[str] = Field(description="This is a optional keyword argument")
    e: str = Field(None, description="This is a optional keyword argument with alias", alias="eee")
    f: str = Field("default", description="This is a optional keyword argument")
    g: str = Field("default", description="This is a optional keyword argument with alias", alias="-G")


cliargs = pa.parse(Temp, program_name="Example program", description="The example program description")

print(cliargs)


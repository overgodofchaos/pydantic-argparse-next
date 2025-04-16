from pydantic import BaseModel
import pydantic_argparse_new as pa


class Temp(BaseModel):
    a: str = pa.Arg(..., description="This is a required positional argument")
    b: str = pa.Arg("default", description="This is a optional positional argument")

    # The pa.KwArg object is the same as just pydantic.Field.
    # Either one can always be used, it makes no difference.
    c: str = pa.KwArg(..., description="This is a required keyword argument")
    d: str = pa.KwArg(None, description="This is a optional keyword argument")


cliargs = pa.parse(
    Temp,
    program_name="Example program",
    description="The example program description",
    epilog="The example program epilog"
)

print(cliargs)

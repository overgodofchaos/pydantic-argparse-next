from pydantic import BaseModel
import pydantic_argparse_new as pa


class Subcommand1(BaseModel):
    c: str = pa.KwArg(..., description="This is required keyword argument in subcommand")


class Subcommand2(BaseModel):
    d: str = pa.KwArg(..., description="This is required keyword argument in subcommand")


class Temp(BaseModel):
    a: str = pa.KwArg(..., description="This is required keyword argument")
    b: str = pa.KwArg("default", description="This is optional keyword argument")

    # Subcommands must be made optional in any way
    # Regardless, at least one subcommand must be selected in the CLI unless otherwise configured.
    sub1: Subcommand1 = pa.Subcommand(None, description="This is a subcommand")
    sub2: Subcommand2 = pa.Subcommand(None, description="This is a subcommand")


cliargs = pa.parse(
    Temp,
    program_name="Example program",
    description="The example program description",
    subcomand_required=False
)

print(cliargs)

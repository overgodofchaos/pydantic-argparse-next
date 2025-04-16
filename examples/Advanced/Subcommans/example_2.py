from pydantic import BaseModel
import pydantic_argparse_next as pa


class Subcommand1(BaseModel):
    c: str = pa.KwArg(..., description="This is required keyword argument in subcommand")


class Subcommand2(BaseModel):
    d: str = pa.KwArg(..., description="This is required keyword argument in subcommand")


class Temp(BaseModel):
    a: str = pa.KwArg(..., description="This is required keyword argument")
    b: str = pa.KwArg("default", description="This is optional keyword argument")

    # Subcommands must be made optional in any way
    # Regardless, at least one subcommand must be selected in the CLI unless otherwise configured.
    sub1: Subcommand1 = pa.Subcommand(
        None,
        description="This is a subcommand",
        long_description="This is a long description for sub1 in class Temp.",
        epilog="This is a epilog for sub1 in class Temp."
    )
    sub2: Subcommand2 = pa.Subcommand(
        None,
        description="This is a subcommand",
        long_description="This is a long description for sub2 in class Temp.",
        epilog="This is a epilog for sub2 in class Temp."
    )


cliargs = pa.parse(Temp, program_name="Example program", description="The example program description")

print(cliargs)

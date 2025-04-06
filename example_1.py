from pydantic_argparser_zero_tst import Arg, KwArg, Subcommand, parse
from pydantic import BaseModel, Field
from typing import Optional, Literal
from enum import Enum


class Choices(Enum):
    example1 = 1
    example2 = 2


class Subcommand1(BaseModel):
    subarg: str = KwArg(..., description="It is a subcommand argument")


class Subcommand2(BaseModel):
    subarg: str = KwArg(..., description="It is a subcommand argument")


class Commands(BaseModel):
    # Required positional arguments
    arg1: str = Arg(..., description="It is a required positional argument.")

    # Optional positional arguments
    arg2: str = Arg("example", description="It is a optional positional argument.")
    arg3: Optional[str] = Arg(..., description="It is a optional positional argument.")

    # Required keyword arguments
    arg4: str = KwArg(..., description="It is a required keyword argument.")
    arg5: str = Field(..., description="It is a required keyword argument.")

    # Optional keyword arguments
    arg6: str = KwArg("example", description="It is a optional keyword argument.")
    arg7: str = Field("example", description="It is a optional keyword argument.")
    arg8: Optional[str] = KwArg(..., description="It is a optional keyword argument.")
    arg9: Optional[str] = Field(..., description="It is a optional keyword argument.")

    # Choice arguments (can be positional or keyword)
    arg10: Literal["example1", "example2"] = KwArg("example1", description="It is a choice keyword argument.")
    arg11: Choices = KwArg(Choices.example1, description="It is a choice keyword argument.")

    # Store true argument (can be only optional keyword)
    arg12: bool = KwArg(False, description="It is a store true argument.")

    # Store false argument (can be only optional keyword)
    arg13: bool = KwArg(True, description="It is a store false argument.")

    # Subcommands
    subcommand1: Optional[Subcommand1] = Subcommand(description="It is a subcommand")
    subcommand2: Optional[Subcommand2] = Subcommand(description="It is a subcommand")


args = ["example",
        "example2",
        "example3",
        "--arg4", "example4",
        "--arg5", "example5",
        "--arg6", "example6",
        "--arg7", "example7",
        "--arg8", "example8",
        "--arg9", "example9",
        "--arg10", "example2",
        "--arg11", "example2",
        "--arg12",
        "--arg13",
        "subcommand1",
        "--subarg", "sub_example"
        ]


commands = parse(Commands, args)

print(commands)

commands = parse(Commands, ["--help"])
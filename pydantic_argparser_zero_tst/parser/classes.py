from pydantic import BaseModel
from pydantic_core import PydanticUndefined
from typing import Any
from typing import Literal





# noinspection PyRedeclaration
class BaseModel(BaseModel):
    class Config:
        validate_assignment = True


class ExtraInfoArgument(BaseModel):
    required: bool = True


class ExtraInfoOption(BaseModel):
    required: bool = True


class ExtraInfoSubcommand(BaseModel):
    pass


class ParserConfig(BaseModel):
    prog: str | None = None
    usage: str | None = None
    description: str | None = None
    epilog: str | None = None
    argument_default: Any | None = None
    add_help: bool = True
    allow_abbrev: bool = True
    exit_on_error: bool = True


class SubparserConfig(BaseModel):
    title: str = None
    description: str | None = None
    prog: str = None
    required: bool = True
    help: str | None = None


def subparserconfig(
        title: str | None = None,
        description: str | None = None,
        prog: str | None = None,
        required: bool = True,
        help: str | None = None,
):
    return SubparserConfig(title=title, description=description, prog=prog, required=required, help=help)


def parserconfig(
        prog: str = None,
        usage: str = None,
        description: str = None,
        epilog: str = None,
        argument_default: Any = None,
        add_help: bool = True,
        allow_abbrev: bool = True,
        exit_on_error: bool = True,
):
    return ParserConfig(prog=prog, usage=usage, description=description, epilog=epilog,
                        argument_default=argument_default, add_help=add_help,
                        allow_abbrev=allow_abbrev, exit_on_error=exit_on_error)


class PydanticArgparseError(Exception):
    pass


class ArgumentBase(BaseModel):
    attribute_name: str
    description: str | None = None
    required: bool = True
    default: Any | None = None


class Argument(ArgumentBase):
    pass


class Option(ArgumentBase):
    alias: str | None = None


class Subcommand(BaseModel):
    attribute_name: str
    description: str | None = None
    model: BaseModel


class Parser(BaseModel):
    arguments: list[Argument] = []
    options: list[Option] = []
    subcommands: list[Subcommand] = []



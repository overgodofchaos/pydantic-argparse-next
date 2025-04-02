import pydantic
from pydantic import BaseModel
from pydantic_core import PydanticUndefined
from typing import Any, Type
# noinspection PyUnresolvedReferences
from typing import Literal
from .utils import find_any


# noinspection PyRedeclaration
class BaseModel(BaseModel):
    class Config:
        validate_assignment = True


class ExtraInfoArgument(BaseModel):
    pass


class ExtraInfoKeywordArgument(BaseModel):
    pass


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


# noinspection PyShadowingBuiltins
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


class PydanticArgparserError(Exception):
    pass


class ArgumentBase(BaseModel):
    attribute_name: str
    description: str | None = None
    required: bool = True
    default: Any = PydanticUndefined

    def model_post_init(self, context: Any) -> None:
        print("MODEL POST INIT")
        print(self)
        if self.default is not PydanticUndefined:
            self.required = False
        else:
            self.required = True


class Argument(ArgumentBase):
    pass


class KeywordArgument(ArgumentBase):
    alias: str | None = None

    @property
    def options_names(self):
        names = []

        name = self.attribute_name.replace("_", "-")
        names.append(f"--{name}")

        if self.alias is not None:
            alias = self.alias.replace("_", "-")
            if alias.startswith("-"):
                names.append(f"{alias}")
            else:
                names.append(f"--{alias}")

        return names


class Subcommand(BaseModel):
    attribute_name: str
    description: str | None = None
    model: BaseModel


class Parser(BaseModel):
    arguments: list[Argument] = []
    options: list[KeywordArgument] = []
    subcommands: list[Subcommand] = []
    model: Type[pydantic.BaseModel]

    def resolve(self, args: list[str]) -> BaseModel:
        schema = {}

        for argument in self.arguments:
            if args[0].startswith("-") is False:
                schema[argument.attribute_name] = args[0]
                args.pop(0)
            else:
                if argument.required:
                    raise PydanticArgparserError(f"Argument {argument.attribute_name} is required")

        if len(args) > 0 and args[0].startswith("-") is False:
            raise PydanticArgparserError(f"Argument {args[0]} is not defined")

        for option in self.options:
            option_position = find_any(args, option.options_names)

            if option_position == -1:
                if option.required:
                    raise PydanticArgparserError(f"Option {option.options_names[0]} is required")
                else:
                    continue
            else:
                schema[option.attribute_name] = args[option_position + 1]

        return self.model(**schema)

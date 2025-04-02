import pydantic
from pydantic import BaseModel
from pydantic_core import PydanticUndefined
from typing import Any, Type
# noinspection PyUnresolvedReferences
from typing import Literal
from .utils import find_any
from rich.console import Console
from rich.panel import Panel
from rich.table import Table, box
from rich.style import Style
import sys


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
    alias: str | None = None
    description: str | None = None
    default: Any = PydanticUndefined

    @property
    def required(self) -> bool:
        if self.default is not PydanticUndefined:
            return False
        else:
            return True


class Argument(ArgumentBase):
    pass


class KeywordArgument(ArgumentBase):

    @property
    def keyword_arguments_names(self):
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
    alias: str | None = None
    description: str | None = None
    model: BaseModel


class Parser(BaseModel):
    program_name: str = "Default program name"
    program_description: str = "Default program description"

    required_arguments: list[Argument] = []
    optional_arguments: list[Argument] = []
    required_keyword_arguments: list[KeywordArgument] = []
    optional_keyword_arguments: list[KeywordArgument] = []
    subcommands: list[Subcommand] = []
    model: Type[pydantic.BaseModel]

    def help(self):
        console = Console()

        program = Panel(
            self.program_description,
            title_align="left",
            title=self.program_name,
            border_style="bold yellow"
        )

        console.print(program)

        if len(self.required_arguments) > 0:
            arguments_table = Table(show_header=False, box=None)

            for argument in self.required_arguments:
                if argument.alias:
                    alias = f"({argument.alias})"
                else:
                    alias = ""

                arguments_table.add_row(
                    argument.attribute_name,
                    alias,
                    argument.description
                )
            arguments_panel = Panel(
                arguments_table,
                title_align="left",
                title="Required positional arguments",
                border_style="bold blue"
            )

            console.print(arguments_panel)

        if len(self.optional_arguments) > 0:
            arguments_table = Table(show_header=False, box=None)
            for argument in self.optional_arguments:

                default = f"[Default: {str(argument.default)}]"
                if argument.alias:
                    alias = f"({argument.alias})"
                else:
                    alias = ""

                arguments_table.add_row(
                    argument.attribute_name,
                    alias,
                    argument.description,
                    default
                )
            arguments_panel = Panel(
                arguments_table,
                title_align="left",
                title="Optional positional arguments",
                border_style="bold blue"
            )

            console.print(arguments_panel)

        if len(self.required_keyword_arguments) > 0:
            arguments_table = Table(show_header=False, box=None)
            for argument in self.required_keyword_arguments:
                names = argument.keyword_arguments_names
                name = names[0]

                if len(names) > 1:
                    alias = f"({names[1]})"
                else:
                    alias = ""

                arguments_table.add_row(
                    name,
                    alias,
                    argument.description
                )
            arguments_panel = Panel(
                arguments_table,
                title_align="left",
                title="Required keyword arguments",
                border_style="bold blue"
            )

            console.print(arguments_panel)

        if len(self.optional_keyword_arguments) > 0:
            arguments_table = Table(show_header=False, box=None)
            for argument in self.optional_keyword_arguments:
                names = argument.keyword_arguments_names
                name = names[0]

                default = f"[Default: {str(argument.default)}]"

                if len(names) > 1:
                    alias = f"({names[1]})"
                else:
                    alias = ""

                arguments_table.add_row(
                    name,
                    alias,
                    argument.description,
                    default
                )
            arguments_panel = Panel(
                arguments_table,
                title_align="left",
                title="Optional keyword arguments",
                border_style="bold blue"
            )

            console.print(arguments_panel)




        sys.exit(0)


    def resolve(self, args: list[str]) -> BaseModel:
        schema = {}

        # Help
        if find_any(args, ["--help", "-H"]) != -1:
            self.help()

        # Required positional arguments
        for argument in self.required_arguments:
            if args[0].startswith("-") is False:
                name = argument.attribute_name if argument.alias is None else argument.alias
                schema[name] = args[0]
                args.pop(0)
            else:
                raise PydanticArgparserError(f"Argument {argument.attribute_name} is required")

        # Optional positional arguments
        for argument in self.optional_arguments:
            if args[0].startswith("-") is False:
                name = argument.attribute_name if argument.alias is None else argument.alias
                schema[name] = args[0]
                args.pop(0)
            else:
                break

        # Excess arguments
        if len(args) > 0 and args[0].startswith("-") is False:
            raise PydanticArgparserError(f"Argument {args[0]} is not defined")

        # Required keyword arguments
        for argument in self.required_keyword_arguments:
            argument_position = find_any(args, argument.keyword_arguments_names)

            if argument_position == -1:
                raise PydanticArgparserError(f"Option {argument.keyword_arguments_names[0]} is required")
            else:
                name = argument.attribute_name if argument.alias is None else argument.alias
                schema[name] = args[argument_position + 1]

        # Optional keyword arguments
        for argument in self.optional_keyword_arguments:
            argument_position = find_any(args, argument.keyword_arguments_names)
            if argument_position == -1:
                continue
            else:
                name = argument.attribute_name if argument.alias is None else argument.alias
                schema[name] = args[argument_position + 1]

        print(schema)
        return self.model(**schema)

import pydantic
from pydantic import BaseModel
from pydantic_core import PydanticUndefined
# noinspection PyUnresolvedReferences,PyProtectedMember
from pydantic.fields import FieldInfo
from typing import Any, Type
# noinspection PyUnresolvedReferences
from typing import Literal, Optional, Union
from .utils import find_any
from rich.console import Console, Group
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
    __filed_info__: FieldInfo = None
    __extra_info__: Union[ExtraInfoArgument, ExtraInfoKeywordArgument, ExtraInfoSubcommand] = None

    def __init__(self,
                 *args,
                 attribute_name: str,
                 field_info: FieldInfo,
                 extra_info: Union[ExtraInfoArgument, ExtraInfoKeywordArgument, ExtraInfoSubcommand],
                 **kwargs):
        super().__init__(attribute_name=attribute_name, **kwargs)
        self.__filed_info__ = field_info
        self.__extra_info__ = extra_info

    @property
    def alias(self) -> str | None:
        return self.__filed_info__.alias

    @property
    def description(self) -> str:
        if self.__filed_info__.description:
            return self.__filed_info__.description
        else:
            return ""

    @property
    def default(self) -> Any:
        return self.__filed_info__.default

    @property
    def required(self) -> bool:
        if self.default is not PydanticUndefined:
            return False
        else:
            return True

    @property
    def help_text(self) -> list[str]:
        if isinstance(self, Argument):
            name = self.attribute_name
            alias = "" if self.alias is None else f"({self.alias})"
        elif isinstance(self, KeywordArgument):
            name = self.keyword_arguments_names[0]
            alias = "" if self.alias is None else f"({self.keyword_arguments_names[1]})"
        else:
            raise IOError(f"Type {type(self)} not recognized")

        default = "" if self.required else f"[Default: {str(self.default)}]"
        description = self.description

        result = [
            name,
            alias,
            description,
            default,
        ]
        return result


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
    __field_info__: FieldInfo = None


class Parser(BaseModel):
    program_name: str = "Default program name"
    program_description: str = "Default program description"
    program_epilog: str = "Default program epilog"

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

        def get_help_panel(x: list[Argument | KeywordArgument], title: str) -> Panel:
            table = Table(show_header=False, box=None)
            for arg in x:
                table.add_row(
                    *arg.help_text,
                )

            panel = Panel(
                table,
                title_align="left",
                title=title,
                border_style="bold yellow"

            )
            return panel

        x = [
            [self.required_arguments, self.optional_arguments, "Positianal arguments"],
            [self.required_keyword_arguments, self.optional_keyword_arguments, "Keyword arguments"]
        ]

        for s in x:
            arguments = []
            if self.required_arguments:
                arguments.append(get_help_panel(s[0], title="Required"))
            if self.optional_arguments:
                arguments.append(get_help_panel(s[1], title="Optional"))

            if arguments:
                positional_arguments = Panel(
                    Group(*arguments),
                    title_align="left",
                    title=s[2],
                    border_style="bold blue"
                )

                console.print(positional_arguments)

        program = Panel(
            self.program_epilog,
            title_align="left",
            title=None,
            border_style="bold yellow"
        )

        console.print(program)

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

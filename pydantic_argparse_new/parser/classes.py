import pydantic
from pydantic import BaseModel, ConfigDict
from pydantic_core import PydanticUndefined
# noinspection PyUnresolvedReferences,PyProtectedMember
from pydantic.fields import FieldInfo
from typing import Any, Type
# noinspection PyUnresolvedReferences
from typing import Literal, Optional, Union
from typing import Type, Any, get_args, get_origin
from .utils import find_any
from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table, box
from rich.style import Style
import sys
from enum import Enum
from pathlib import Path
import types


# noinspection PyRedeclaration
class BaseModel(BaseModel):
    model_config = ConfigDict(
        validate_assignment=True,
    )


class ExtraInfoArgument(BaseModel):
    pass


class ExtraInfoKeywordArgument(BaseModel):
    pass


class ExtraInfoSubcommand(BaseModel):
    pass


class ParserConfig(BaseModel):
    program_name: str | None = None
    description: str | None = None
    epilog: str | None = None
    subcommand_required: bool = True


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
        program_name: str = None,
        description: str = None,
        epilog: str = None,
        subcommand_required: bool = True
):
    return ParserConfig(program_name=program_name, description=description, epilog=epilog,
                        subcommand_required=subcommand_required)


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
        self.argument_validate()

    def argument_validate(self):
        pass

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
    def type(self):
        type_ = self.__filed_info__.annotation
        if self.optional_annotation:
            return get_args(type_)[0]
        else:
            return type_

    @property
    def optional_annotation(self):
        type_ = self.__filed_info__.annotation
        if str(type_).find("Optional") != -1:
            return True
        elif (types.UnionType is get_origin(type_) and
                types.NoneType in get_args(type_)):
            return True
        else:
            return False

    @property
    def required(self) -> bool:
        if self.default is not PydanticUndefined or self.optional_annotation is True:
            return False
        else:
            return True

    @property
    def choices(self) -> list[str]:
        if self.action != "choice":
            raise PydanticArgparserError("Choices list available only for choice argument")
        if get_origin(self.type) is Literal:
            choices = get_args(self.type)
            return [str(x) for x in choices]
        elif issubclass(self.type, Enum):
            # noinspection PyProtectedMember
            choices = self.type._member_names_
            return [str(x) for x in choices]
        else:
            raise PydanticArgparserError(f"Type {self.type} is not supported for choices")

    @property
    def action(self) -> str:
        if self.type is bool:
            if self.default is False:
                return "store_true"
            elif self.default is True:
                return "store_false"
            else:
                raise PydanticArgparserError("Default for boolean argument must be True or False")
        if get_origin(self.type) is Literal or issubclass(self.type, Enum):
            return "choice"

        return "normal"

    @property
    def help_text(self) -> list[str]:
        if isinstance(self, Argument):
            name = self.attribute_name
            alias = "" if self.alias is None else f"({self.alias})"
        elif isinstance(self, KeywordArgument):
            name = self.keyword_arguments_names[0]
            alias = "" if self.alias is None else f"({self.keyword_arguments_names[1]})"
        elif isinstance(self, Subcommand):
            name = self.attribute_name
            alias = "" if self.alias is None else f"({self.alias})"
        else:
            raise IOError(f"Type {type(self)} not recognized")

        if self.action == "choice" and isinstance(self.default, Enum):
            default = "" if self.required else f"[Default: {str(self.default.name)}]"
        else:
            if self.default is PydanticUndefined and not self.required:
                default = "[Default: None]"
            else:
                default = "" if self.required else f"[Default: {str(self.default)}]"

        description = self.description

        match self.action:
            case "choice":
                input_ = "{" + f"{'|'.join(self.choices)}" + "}"
            case "store_false" | "store_true":
                input_ = "STORE"
            case _:
                input_ = "TEXT"

        if isinstance(self, Subcommand):
            input_ = ""
            default = ""

        result = [
            name,
            alias,
            input_,
            description,
            default,
        ]
        return result

    def resolve_choice(self, x: str) -> str | Enum:
        if get_origin(self.type) is Literal:
            return x
        elif issubclass(self.type, Enum):
            return self.type[x]
        else:
            raise PydanticArgparserError(f"resolve_choice method only for choice argument")


class Argument(ArgumentBase):

    def argument_validate(self):
        if self.type is bool:
            raise PydanticArgparserError("Positional argument can't be a boolean")


class KeywordArgument(ArgumentBase):

    def argument_validate(self):
        if (self.type is bool and
                (self.default is not False and
                 self.default is not True)):
            print(self.default, self.attribute_name)
            raise PydanticArgparserError("Boolean argument must have a default boolean value")

    @property
    def keyword_arguments_names(self):
        names = []

        name = self.attribute_name.replace("_", "-")
        if self.action == "store_false":
            name = f"no-{name}"
        names.append(f"--{name}")

        if self.alias is not None:
            alias = self.alias.replace("_", "-")
            if self.action == "store_false":
                alias = f"no-{alias}"
                names.append(f"--{alias}")
            else:
                if alias.startswith("-") is False:
                    names.append(f"--{alias}")
                else:
                    names.append(f"{alias}")

        return names


class Subcommand(ArgumentBase):
    pass


class Parser(BaseModel):
    # program_name: str = "Default program name"
    # program_description: str = "Default program description"
    # program_epilog: str = "Default program epilog"

    required_arguments: list[Argument] = []
    optional_arguments: list[Argument] = []
    required_keyword_arguments: list[KeywordArgument] = []
    optional_keyword_arguments: list[KeywordArgument] = []
    subcommands: list[Subcommand] = []
    model: Type[pydantic.BaseModel]
    args: list[str]
    subcommand: Subcommand | None = None

    @property
    def is_subcommand(self) -> bool:
        if self.subcommand:
            return True
        else:
            return False

    @property
    def subcommand_name(self) -> str:
        if self.subcommand:
            if self.subcommand.alias:
                return self.subcommand.alias
            else:
                return self.subcommand.attribute_name
        else:
            raise PydanticArgparserError(f"Method subcommand_name available only for subcommand")

    @property
    def program_name(self) -> str:
        if self.is_subcommand:
            script_path = Path(sys.argv[0])
            script_name = script_path.stem
            return f"{script_name} {self.subcommand_name}"

        if self._parserconfig.program_name:
            return self._parserconfig.program_name
        else:
            script_path = Path(sys.argv[0])
            script_name = script_path.stem
            return script_name

    @property
    def program_description(self) -> str | None:
        description = self._parserconfig.description
        if not description and self.is_subcommand:
            description = self.subcommand.description
        return description

    @property
    def program_epilog(self) -> str | None:
        return self._parserconfig.epilog

    @property
    def _parserconfig(self) -> ParserConfig:
        if hasattr(self.model, "__parserconfig__"):
            return self.model.__parserconfig__
        else:
            return ParserConfig()

    def model_post_init(self, context: Any) -> None:
        model = self.model
        model_fields = model.model_fields

        for field in model_fields.keys():
            field_info: FieldInfo = model_fields[field]

            attribute_name = field

            try:
                extra_info = field_info.json_schema_extra["pydantic_argparser_zero_extra"]
            except (KeyError, TypeError):
                extra_info = ExtraInfoKeywordArgument()

            if isinstance(extra_info, ExtraInfoArgument):
                # noinspection PyArgumentList
                argument = Argument(
                    attribute_name=attribute_name,
                    field_info=field_info,
                    extra_info=extra_info,
                )
                if argument.required:
                    self.required_arguments.append(argument)
                else:
                    self.optional_arguments.append(argument)

            if isinstance(extra_info, ExtraInfoKeywordArgument):
                # noinspection PyArgumentList
                argument = KeywordArgument(
                    attribute_name=attribute_name,
                    field_info=field_info,
                    extra_info=extra_info,
                )
                if argument.required:
                    self.required_keyword_arguments.append(argument)
                else:
                    self.optional_keyword_arguments.append(argument)

            if isinstance(extra_info, ExtraInfoSubcommand):
                # noinspection PyArgumentList
                subcommand = Subcommand(
                    attribute_name=attribute_name,
                    field_info=field_info,
                    extra_info=extra_info,
                )
                self.subcommands.append(subcommand)

    def _get_usage_text(self):
        script_path = Path(sys.argv[0])
        script_name = script_path.stem
        script_usage = script_name

        if self.is_subcommand:
            script_usage += f" {self.subcommand_name}"

        if len(self.required_arguments) > 0:
            script_usage += f" [REQ ARGS]"
        if len(self.optional_arguments) > 0:
            script_usage += f" [OPT ARGS]"
        if len(self.required_keyword_arguments) > 0 or len(self.optional_keyword_arguments) > 0:
            script_usage += f" [KWARGS]"
        if len(self.subcommands) > 0:
            script_usage += f" [SUBCOMMAND]"
        return script_usage

    def help(self):
        console = Console()

        # Program name and description
        if self.program_description:
            program = Panel(
                self.program_description,
                title_align="left",
                title=self.program_name,
                border_style="bold yellow"
            )
        else:
            program = Panel(
                self.program_name,
                title_align="left",
                title=None,
                border_style="bold yellow"
            )

        console.print(program)

        # Usage
        usage = Panel(
            self._get_usage_text(),
            title_align="left",
            title="Usage",
            border_style="bold yellow"
        )
        console.print(usage)

        # Arguments
        def get_help_panel(x: list[Argument | KeywordArgument | Subcommand], title: str | None) -> Panel:
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
            [self.required_keyword_arguments, self.optional_keyword_arguments, "Keyword arguments"],
        ]

        for s in x:
            arguments = []
            if s[0]:
                arguments.append(get_help_panel(s[0], title="Required"))
            if s[1]:
                arguments.append(get_help_panel(s[1], title="Optional"))

            if arguments:
                positional_arguments = Panel(
                    Group(*arguments),
                    title_align="left",
                    title=s[2],
                    border_style="bold blue"
                )

                console.print(positional_arguments)

        # Subcommands
        if len(self.subcommands) > 0:
            subcommands = Panel(
                get_help_panel(self.subcommands, title=None),
                title_align="left",
                title="Subcommands",
                border_style="bold blue"
            )
            console.print(subcommands)

        # Epilog
        if self.program_epilog:
            epilog = Panel(
                self.program_epilog,
                title_align="left",
                title=None,
                border_style="bold yellow"
            )

            console.print(epilog)

        sys.exit(0)

    def resolve(self, subcommand_: bool = False) -> BaseModel | dict:
        schema = {}
        args = self.args

        # Help
        if find_any(args, ["--help", "-H"]) != -1:
            self.help()

        # Separate subcommands
        if len(self.subcommands) > 0:
            subcommand_position = find_any(args, [x.attribute_name for x in self.subcommands])
            if subcommand_position > -1:
                args = self.args[:subcommand_position]
                subcommand_args = self.args[subcommand_position + 1:]
                subcommand_name = self.args[subcommand_position]
            else:
                if self._parserconfig.subcommand_required:
                    raise PydanticArgparserError("Subcommand required")
                else:
                    subcommand_args = []
                    subcommand_name = None
                    pass

        # Help subcommand
        try:
            # noinspection PyUnboundLocalVariable
            if find_any(subcommand_args, ["--help", "-H"]) != -1:
                for subcommand in self.subcommands:
                    # noinspection PyUnboundLocalVariable
                    if subcommand.attribute_name == subcommand_name:
                        Parser(
                            model=subcommand.type,
                            args=subcommand_args,
                            subcommand=subcommand
                        ).resolve()
        except NameError:
            pass

        # Positional arguments
        for argument in self.required_arguments + self.optional_arguments:
            name = argument.attribute_name if argument.alias is None else argument.alias
            if len(args) > 0 and args[0].startswith("-") is False:
                if argument.action == "choice":
                    schema[name] = argument.resolve_choice(args[0])
                else:
                    schema[name] = args[0]
                args.pop(0)
            else:
                if argument.required:
                    raise PydanticArgparserError(f"Argument {argument.attribute_name} is required")
                continue

        # Excess positional arguments
        if len(args) > 0 and args[0].startswith("-") is False:
            raise PydanticArgparserError(f"Argument {args[0]} is not defined")

        # Keyword argumwnts
        for argument in self.required_keyword_arguments + self.optional_keyword_arguments:
            argument_position = find_any(args, argument.keyword_arguments_names)
            print(argument.keyword_arguments_names)

            if argument_position == -1:
                if argument.required:
                    raise PydanticArgparserError(f"Keyword argument {argument.keyword_arguments_names[0]} is required")
                continue

            name = argument.attribute_name if argument.alias is None else argument.alias

            match argument.action:
                case "normal":
                    schema[name] = args[argument_position + 1]
                case "store_true":
                    schema[name] = True
                case "store_false":
                    schema[name] = False
                case "choice":
                    schema[name] = argument.resolve_choice(args[argument_position + 1])

        # Processing optional annotation
        for argument in self.optional_arguments + self.optional_keyword_arguments:
            name = argument.attribute_name if argument.alias is None else argument.alias
            if argument.action == "normal":
                if name not in schema:
                    if argument.optional_annotation and argument.default is PydanticUndefined:
                        schema[name] = None

        # Subcommands
        for subcommand in self.subcommands:
            if subcommand.attribute_name == subcommand_name:
                schema[subcommand.attribute_name] = Parser(
                    model=subcommand.type,
                    args=subcommand_args,
                    subcommand=subcommand
                ).resolve()
            else:
                schema[subcommand.attribute_name] = None

        # print(schema)

        if self.is_subcommand:
            return schema
        else:
            return self.model(**schema)

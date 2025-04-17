import pydantic
from pydantic import BaseModel, ConfigDict
from pydantic_core import PydanticUndefined
# noinspection PyUnresolvedReferences,PyProtectedMember
from pydantic.fields import FieldInfo
from typing import Any, Type
# noinspection PyUnresolvedReferences
from typing import Literal, Optional, Union
from typing import Type, Any, get_args, get_origin, cast
from .utils import find_any
from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table, box
from rich.style import Style
import sys
from enum import Enum
from pathlib import Path
import types
from .classes import Argument, KeywordArgument, Subcommand, PydanticArgparserError
from .classes import ParserConfig, ExtraInfoKeywordArgument
from .classes import ExtraInfoArgument, ExtraInfoSubcommand, SelectedSubcommand


# noinspection PyRedeclaration
class BaseModel(BaseModel):
    model_config = ConfigDict(
        validate_assignment=True,
    )


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
    prefix: str | None = None

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.model_post_init_2()

    def model_post_init_2(self):
        if self.is_subcommand:
            if hasattr(self.model, "__parserconfig__"):
                if not isinstance(self.model.__parserconfig__, ParserConfig):
                    self.model.__parserconfig__ = ParserConfig()
            else:
                self.model.__parserconfig__ = ParserConfig()

            extra_info = self.subcommand.__extra_info__

            if extra_info.long_description:
                self.model.__parserconfig__.description = extra_info.long_description
            if extra_info.epilog:
                self.model.__parserconfig__.epilog = extra_info.epilog

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
    def _script_name(self) -> str:
        script_path = Path(sys.argv[0])
        script_name = script_path.stem
        return script_name

    @property
    def name(self) -> str:
        if self.is_subcommand:
            return f"{self.prefix} {self.subcommand_name}"

        if self._parserconfig.program_name:
            return self._parserconfig.program_name
        else:
            return self._script_name

    @property
    def program_description(self) -> str | None:
        description = self._parserconfig.description
        if not description and self.is_subcommand:
            description = self.subcommand.description
        return description

    @property
    def program_epilog(self) -> str | None:
        return self._parserconfig.epilog

    # @property
    # def subcommand_destionation(self) -> str:
    #     name = self._parserconfig.subcommand_destination
    #     if name.startswith("__") and name.endswith("__"):
    #         return name
    #     elif name.startswith("_") or name.endswith("_"):
    #         raise PydanticArgparserError(f"Incorrect subcommand_destionation {name}")
    #     else:
    #         return f"__{name}__"

    @property
    def _parserconfig(self) -> ParserConfig:
        if hasattr(self.model, "__parserconfig__"):
            return self.model.__parserconfig__
        else:
            return ParserConfig()

    def get_prefix(self):
        if self.is_subcommand:
            return f"{self.prefix} {self.subcommand_name}"
        else:
            return f"{self._script_name}"

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

    def show_help(self):
        console = Console()

        # Program name and description
        if self.program_description:
            program = Panel(
                self.program_description,
                title_align="left",
                title=self.name,
                border_style="bold yellow"
            )
        else:
            program = Panel(
                self.name,
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

    def resolve(self) -> BaseModel:
        schema = {}
        args = self.args

        subcommand_args = []
        subcommand_name = None

        # Separate subcommands
        if len(self.subcommands) > 0:
            subcommand_position = find_any(self.args, [x.attribute_name for x in self.subcommands])
            if subcommand_position > -1:
                args = self.args[:subcommand_position]
                subcommand_args = self.args[subcommand_position + 1:]
                subcommand_name = self.args[subcommand_position]

        # Help
        if find_any(args, ["--help", "-H"]) != -1:
            self.show_help()
            sys.exit(0)
            # noinspection PyTypeChecker,PyUnreachableCode
            return  # For pytest

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
                            subcommand=subcommand,
                            prefix=self.get_prefix()
                        ).resolve()
                # noinspection PyTypeChecker,PyUnreachableCode
                return  # For pytest
        except NameError:
            pass

        # Subcommand required check
        if len(self.subcommands) > 0:
            subcommand_position = find_any(self.args, [x.attribute_name for x in self.subcommands])
            if subcommand_position == -1 and self._parserconfig.subcommand_required:
                raise PydanticArgparserError("Subcommand required")

        # Positional arguments
        for argument in self.required_arguments + self.optional_arguments:
            name = argument.attribute_name if argument.alias is None else argument.alias
            if len(args) > 0 and args[0].startswith("-") is False:
                match argument.action:
                    case "normal":
                        schema[name] = args[0]
                        args.pop(0)
                    case "choice":
                        schema[name] = argument.resolve_choice(args[0])
                        args.pop(0)
                    case "variadic":
                        values = []
                        for i in range(argument.variadic_max_args):
                            values.append(args[0])
                            args.pop(0)
                        schema[name] = values
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

            if argument_position == -1:
                if argument.required:
                    raise PydanticArgparserError(f"Keyword argument {argument.keyword_arguments_names[0]} is required")
                continue

            name = argument.attribute_name if argument.alias is None else argument.alias

            # print(argument.action)

            match argument.action:
                case "normal":
                    schema[name] = args[argument_position + 1]
                    args.pop(argument_position)
                    args.pop(argument_position)
                case "store_true":
                    schema[name] = True
                    args.pop(argument_position)
                case "store_false":
                    schema[name] = False
                    args.pop(argument_position)
                case "choice":
                    schema[name] = argument.resolve_choice(args[argument_position + 1])
                    args.pop(argument_position)
                    args.pop(argument_position)
                case "variadic":
                    args.pop(argument_position)
                    values = []
                    while True:
                        if len(args) == 0:
                            break
                        if args[argument_position].startswith("-"):
                            break
                        values.append(args.pop(argument_position))

                    if len(values) < argument.variadic_min_args or len(values) > argument.variadic_max_args:
                        if argument.variadic_max_args == argument.variadic_min_args:
                            target = f"{argument.variadic_max_args}"
                        else:
                            target = f"between {argument.variadic_min_args} and {argument.variadic_max_args}"

                        raise PydanticArgparserError(f"Argument number of arguments for {argument.name} must"
                                                     f" be {target}. But got {len(values)}.")
                    schema[name] = values

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
                    subcommand=subcommand,
                    prefix=self.get_prefix()
                ).resolve()
            else:
                if subcommand.optional_annotation:
                    schema[subcommand.attribute_name] = None
                else:
                    pass

        # Excess keyword arguments
        for arg in args:
            if arg != subcommand_name:
                raise PydanticArgparserError(f"Unrecognized argument: {arg}")

        # print(schema)

        model = self.model(**schema)
        if subcommand_name:
            setattr(
                model,
                "__subcommand__",
                SelectedSubcommand(
                    name=subcommand_name,
                    value=getattr(model, subcommand_name)
                )
            )
        else:
            setattr(
                model,
                "__subcommand__",
                None
            )

        return model

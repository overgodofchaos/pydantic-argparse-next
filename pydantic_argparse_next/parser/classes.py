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
from collections import deque


# noinspection PyRedeclaration
class BaseModel(BaseModel):
    model_config = ConfigDict(
        validate_assignment=True,
    )


class ExtraInfoArgumetnBase(BaseModel):
    n_args: str | int = "1..."

    @property
    def min_args(self) -> int:
        try:
            min_args = int(self.n_args)
            return min_args
        except ValueError:
            n_args = self.n_args.split("...")
            if len(n_args[0]) == 0:
                return 1
            else:
                min_args = int(n_args[0])
                if min_args == 0:
                    raise PydanticArgparserError("Minimum number of arguments should be greater than 0.")
                else:
                    return min_args

    @property
    def max_args(self) -> int | float:
        try:
            max_args = int(self.n_args)
            return max_args
        except ValueError:
            max_args = self.n_args.split("...")
            if len(max_args[1]) == 0:
                return float("inf")
            else:
                max_args = int(max_args[1])
                if max_args <= self.min_args:
                    raise PydanticArgparserError(
                        f"Maximum number of arguments should be greater than minimum."
                        f" But {self.n_args} was given."
                    )
                else:
                    return max_args


class ExtraInfoArgument(ExtraInfoArgumetnBase):
    pass


class ExtraInfoKeywordArgument(ExtraInfoArgumetnBase):
    pass


class ExtraInfoSubcommand(BaseModel):
    long_description: str | None = None
    epilog: str | None = None
    pass


class ParserConfig(BaseModel):
    program_name: str | None = None
    description: str | None = None
    epilog: str | None = None
    subcommand_required: bool = True
    # subcommand_destination: str = "subcommand"


# class SubparserConfig(BaseModel):
#     title: str = None
#     description: str | None = None
#     prog: str = None
#     required: bool = True
#     help: str | None = None


# # noinspection PyShadowingBuiltins
# def subparserconfig(
#         title: str | None = None,
#         description: str | None = None,
#         prog: str | None = None,
#         required: bool = True,
#         help: str | None = None,
# ):
#     return SubparserConfig(title=title, description=description, prog=prog, required=required, help=help)


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


class SelectedSubcommand(BaseModel):
    name: str
    value: pydantic.BaseModel


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
    def extra_info(self) -> Union[ExtraInfoArgument, ExtraInfoKeywordArgument, ExtraInfoSubcommand]:
        return self.__extra_info__

    @property
    def filed_info(self) -> FieldInfo:
        return self.__filed_info__

    @property
    def name(self):
        if isinstance(self, Argument | Subcommand):
            return self.attribute_name
        elif isinstance(self, KeywordArgument):
            return self.keyword_arguments_names[0]
        else:
            raise TypeError

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
    def type_raw(self):
        type_ = self.__filed_info__.annotation
        if self.optional_annotation:
            return get_args(type_)[0]
        else:
            return type_

    @property
    def type(self):
        type_ = get_origin(self.type_raw)
        if type_ is not None:
            return type_
        else:
            return self.type_raw

    @property
    def type_args(self):
        args = get_args(self.type_raw)
        return args

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
        if self.type is Literal:
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

        if self.type is Literal or issubclass(self.type, Enum):
            return "choice"

        if (
                self.type is list or
                self.type is tuple or
                self.type is set or self.type is frozenset or
                self.type is deque
        ):
            return "variadic"

        return "normal"

    @property
    def variadic_max_args(self) -> int | float:
        if self.action == "variadic":
            if self.type is tuple:
                args_count = len(self.type_args)
                if args_count != 0:
                    return args_count
            return self.extra_info.max_args
        else:
            raise PydanticArgparserError("variadic_max_args is only supported for variadic action")

    @property
    def variadic_min_args(self) -> int:
        if self.action == "variadic":
            if self.type is tuple:
                args_count = len(self.type_args)
                if args_count != 0:
                    return args_count
            return self.extra_info.min_args
        else:
            raise PydanticArgparserError("variadic_min_args is only supported for variadic action")

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
                input_ = str(self.type.__name__).upper()

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
        if self.type is Literal:
            return x
        elif issubclass(self.type, Enum):
            try:
                return self.type[x]
            except KeyError:
                memders = self.type.__members__.keys()
                raise PydanticArgparserError(f"Input should be in [{', '.join(memders)}]"
                                             f" for {self.name}, but {x} was given")
        else:
            raise PydanticArgparserError(f"resolve_choice method only for choice argument")


class Argument(ArgumentBase):

    def argument_validate(self):
        if self.type is bool:
            raise PydanticArgparserError("Positional argument can't be a boolean (store true or store false)")

        match self.action:
            case "variadic":
                min_args = self.variadic_min_args
                max_args = self.variadic_max_args
                if min_args != max_args:
                    raise PydanticArgparserError(f"A positional variadic argument must have a strictly"
                                                 f" defined number of arguments. But {self.extra_info.n_args}"
                                                 f" was given.")


class KeywordArgument(ArgumentBase):

    def argument_validate(self):
        match self.type.__name__:
            case "bool":
                if self.default is not False and self.default is not True:
                    raise PydanticArgparserError("Boolean argument must have a default boolean value"
                                                 " (False for store true or True for store false)")

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
                if alias.startswith("--"):
                    alias = f"no-{alias[2:]}"
                elif alias.startswith("-"):
                    alias = f"no-{alias[1:]}"
                names.append(f"--{alias}")
            else:
                if alias.startswith("-") is False:
                    names.append(f"--{alias}")
                else:
                    names.append(f"{alias}")

        return names


class Subcommand(ArgumentBase):
    pass

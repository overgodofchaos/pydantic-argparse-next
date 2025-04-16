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

        if get_origin(self.type) is Literal or issubclass(self.type, Enum):
            return "choice"

        if (
                get_origin(self.type) is list or
                get_origin(self.type) is tuple
        ):
            return "variadic"

        return "normal"

    @property
    def variadic_max_args(self) -> int | float:
        if self.action == "variadic":
            if get_origin(self.type) is tuple:
                return len(get_args(self.type))
            else:
                return float("inf")
        else:
            raise PydanticArgparserError("variadic_max_args is only supported for variadic action")

    @property
    def variadic_min_args(self) -> int | float:
        if self.action == "variadic":
            if get_origin(self.type) is tuple:
                return len(get_args(self.type))
            else:
                return float("-inf")
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
        if get_origin(self.type) is Literal:
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
        match self.type.__name__:
            case "bool":
                raise PydanticArgparserError("Positional argument can't be a boolean (store true or store false)")
            case "list":
                raise PydanticArgparserError("Positional argument can't be a list")


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




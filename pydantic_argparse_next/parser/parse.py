from pydantic import BaseModel, Field
from pydantic_core import PydanticUndefined
# noinspection PyUnresolvedReferences,PyProtectedMember
from pydantic.fields import FieldInfo
from typing import Type, Any, get_args, get_origin, Literal, TypeVar
import typing
from .classes import ExtraInfoArgument, ExtraInfoSubcommand, ExtraInfoKeywordArgument
from .classes import Argument, KeywordArgument, Subcommand, ParserConfig
from .parser import Parser
import sys


T = TypeVar('T', bound=BaseModel)


def parse(
        model: Type[T],
        program_name: str = None,
        description: str = None,
        epilog: str = None,
        subcomand_required: bool = True,
        version: str = None,
        args: list[str] = None
) -> T:
    if args is None:
        args = sys.argv
        args_ = []
        for arg in args[1:]:
            key, _, value = arg.partition("=")
            args_.append(key)
            if value:
                args_.append(value)
    else:
        args_ = args

    parser = Parser(model=model, args=args_)
    if any([program_name, description, epilog, version]):
        if hasattr(model, "__parserconfig__"):
            if not isinstance(model.__parserconfig__, ParserConfig):
                model.__parserconfig__ = ParserConfig()
        else:
            model.__parserconfig__ = ParserConfig()

        if program_name:
            model.__parserconfig__.program_name = program_name
        if description:
            model.__parserconfig__.description = description
        if epilog:
            model.__parserconfig__.epilog = epilog
        if subcomand_required is False:
            model.__parserconfig__.subcommand_required = subcomand_required
        if version:
            model.__parserconfig__.version = version

    args_model = parser.resolve()

    return args_model

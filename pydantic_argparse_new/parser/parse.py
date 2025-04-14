from pydantic import BaseModel, Field
from pydantic_core import PydanticUndefined
# noinspection PyUnresolvedReferences,PyProtectedMember
from pydantic.fields import FieldInfo
from typing import Type, Any, get_args, get_origin, Literal, TypeVar
import typing
from .classes import ExtraInfoArgument, ExtraInfoSubcommand, ExtraInfoKeywordArgument
from .classes import Argument, KeywordArgument, Subcommand
from .parser import Parser
import sys


T = TypeVar('T', bound=BaseModel)


def parse(model: Type[T], args: list[str] = None) -> T:
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

    # print(parser)

    args_model = parser.resolve()

    return args_model

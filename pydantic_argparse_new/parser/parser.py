from pydantic import BaseModel, Field
from pydantic_core import PydanticUndefined
# noinspection PyUnresolvedReferences,PyProtectedMember
from pydantic.fields import FieldInfo
from typing import Type, Any, get_args, get_origin, Literal
import typing
from .classes import ExtraInfoArgument, ExtraInfoSubcommand, ExtraInfoKeywordArgument
from .classes import Argument, KeywordArgument, Subcommand, Parser
import sys


def parse(model: Type[BaseModel] | BaseModel, args: list[str] = None) -> BaseModel | None:

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






    

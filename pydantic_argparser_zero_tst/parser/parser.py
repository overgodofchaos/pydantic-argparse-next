from pydantic import BaseModel, Field
from pydantic_core import PydanticUndefined
# noinspection PyUnresolvedReferences,PyProtectedMember
from pydantic.fields import FieldInfo
from typing import Type, Any, get_args, get_origin, Literal
import typing
from .classes import ExtraInfoArgument, ExtraInfoSubcommand, ExtraInfoKeywordArgument
from .classes import Argument, KeywordArgument, Subcommand, Parser
import sys


def parse(model: Type[BaseModel] | BaseModel, parser_=None, schema_: dict = None, depth: int = 0) -> BaseModel | None:
    model_fields = model.model_fields

    parser = Parser(model=model)

    for field in model_fields.keys():
        field_info: FieldInfo = model_fields[field]

        attribute_name = field

        try:
            extra_info = field_info.json_schema_extra["pydantic_argparser_zero_extra"]
        except KeyError:
            continue

        if isinstance(extra_info, ExtraInfoArgument):
            argument = Argument(
                attribute_name=attribute_name,
                alias=field_info.alias,
                description=field_info.description,
                default=field_info.default,
                **extra_info.model_dump()
            )
            if argument.required:
                parser.required_arguments.append(argument)
            else:
                parser.optional_arguments.append(argument)

        if isinstance(extra_info, ExtraInfoKeywordArgument):
            argument = KeywordArgument(
                attribute_name=attribute_name,
                alias=field_info.alias,
                description=field_info.description,
                default=field_info.default,
                **extra_info.model_dump()
            )
            if argument.required:
                parser.required_keyword_arguments.append(argument)
            else:
                parser.optional_keyword_arguments.append(argument)

        if isinstance(extra_info, ExtraInfoSubcommand):
            subcommand = Subcommand(
                attribute_name=attribute_name,
                alisa=field_info.alias,
                description=field_info.description,
                model=field_info.annotation,
                **extra_info.model_dump()
            )
            parser.subcommands.append(subcommand)

    # print(parser)

    args = sys.argv
    args_ = []
    for arg in args[1:]:
        key, _, value = arg.partition("=")
        args_.append(key)
        if value:
            args_.append(value)
    print(args_)

    args_model = parser.resolve(args_)

    return args_model






    

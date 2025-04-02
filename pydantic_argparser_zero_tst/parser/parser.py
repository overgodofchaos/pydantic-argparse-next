from pydantic import BaseModel, Field
from pydantic_core import PydanticUndefined
# noinspection PyUnresolvedReferences,PyProtectedMember
from pydantic.fields import FieldInfo
from typing import Type, Any, get_args, get_origin, Literal
import typing
from .classes import ExtraInfoArgument, ExtraInfoOption, ExtraInfoSubcommand
from .classes import Argument, Option, Subcommand, Parser


def parse(model: Type[BaseModel] | BaseModel, parser_=None, schema_: dict = None, depth: int = 0) -> BaseModel | None:
    model_fields = model.model_fields

    parser = Parser()

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
                description=field_info.description,
                default=field_info.default,
                **extra_info.model_dump()
            )
            parser.arguments.append(argument)

        if isinstance(extra_info, ExtraInfoOption):
            option = Option(
                attribute_name=attribute_name,
                alias=field_info.alias,
                description=field_info.description,
                default=field_info.default,
                **extra_info.model_dump()
            )
            parser.options.append(option)

        if isinstance(extra_info, ExtraInfoSubcommand):
            subcommand = Subcommand(
                attribute_name=attribute_name,
                description=field_info.description,
                model=field_info.annotation,
                **extra_info.model_dump()
            )
            parser.subcommands.append(subcommand)

    print(parser)






    

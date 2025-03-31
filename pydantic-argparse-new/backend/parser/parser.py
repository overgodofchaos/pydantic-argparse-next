from argparse import ArgumentParser, Namespace
from pydantic import BaseModel, Field
from typing import Type, Any, get_args, get_origin, Literal
import typing
from .classes import Extra, Argument, ParserConfig, PydanticArgparseError
from .utils import resolve_schema, get_parserconfig


def parse(model: Type[BaseModel] | BaseModel, parser_=None, schema_: dict = None, depth: int = 0) -> BaseModel | None:
    if parser_ is None:
        params = get_parserconfig(model)

        parser = ArgumentParser(**params)
    else:
        parser = parser_

    if schema_ is None:
        schema = dict()
    else:
        schema = schema_

    subparsers = None

    fields = model.model_fields

    arguments = []

    for field in fields.keys():
        schema[field] = None
        field_info = fields[field]

        if str(field_info.annotation).find("Optional") != -1:
            type_ = get_args(field_info.annotation)[0]
        else:
            type_ = field_info.annotation

        if issubclass(type_, BaseModel):
            if subparsers is None:
                subparsers = parser.add_subparsers(dest=f"pydantic-argparser-new_subcommand_depth_{depth}")

            params = get_parserconfig(type_)

            subparser = subparsers.add_parser(field, **params)
            schema[field] = dict()
            parse(
                type_,
                subparser,
                schema[field],
                depth + 1
            )
            continue

        argument = Argument()

        argument.name = field

        if field_info.alias:
            argument.alias = field_info.alias

        if field_info.default is not None:
            argument.required = False
            argument.default = field_info.default

        argument.type = type_

        argument.help = field_info.description

        arguments.append(argument)

        if field_info.json_schema_extra:
            extra = Extra.model_validate(field_info.json_schema_extra)
        else:
            extra = Extra()

        if extra.positional is False:
            argument.positional = False
        else:
            argument.positional = True

        if get_origin(argument.type) is not None:
            # print(get_origin(field_info.annotation))
            if get_origin(field_info.annotation) is list:
                argument.type = get_args(field_info.annotation)[0]

                if len(get_args(field_info.annotation)) == 1:
                    argument.nargs = "*"
                else:
                    argument.nargs = len(get_args(field_info.annotation))
            if str(argument.type).find("Literal") != -1:
                argument.type = str
                argument.choices = list(get_args(field_info.annotation))

        if argument.type is bool:
            if argument.default is False:
                argument.action = "store_true"
            elif argument.default is True:
                argument.action = "store_false"
            else:
                raise IOError("Default must be configured for bool arguments")

    # print(arguments)
    for argument in arguments:
        # print(argument)
        parser.add_argument(
            *argument.names,
            **argument.parametres()
        )

    if parser_ is None:

        args = parser.parse_args()
        resolved_schema = resolve_schema(args, schema)
        return model.model_validate(resolved_schema)


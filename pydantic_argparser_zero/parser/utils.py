from argparse import Namespace
from .classes import ParserConfig, PydanticArgparseError, SubparserConfig
from typing import Type
from pydantic import BaseModel


def resolve_schema(args: Namespace, schema: dict, depth: int = 0):
    keys = list(schema.keys()).copy()
    for key in keys:
        if key in args:
            schema[key] = getattr(args, key)
        else:
            if isinstance(schema[key], dict):
                if (getattr(args, f"pydantic-argparser-new_subcommand_depth_{depth}") is not None and
                        key in getattr(args, f"pydantic-argparser-new_subcommand_depth_{depth}")):
                    schema[key] = resolve_schema(args, schema[key], depth + 1)
                else:
                    schema[key] = None
            else:
                del schema[key]
    return schema


def get_parserconfig(model: BaseModel| Type[BaseModel]) -> dict:
    if hasattr(model, '__parserconfig__'):
        # print(model.__parserconfig__)
        if isinstance(model.__parserconfig__, ParserConfig) is False:
            raise PydanticArgparseError("__parserconfig__ must be an instance of ParserConfig")
        parsms = model.__parserconfig__.model_dump()
    else:
        parsms = {}

    return parsms


def get_subparserconfig(model: BaseModel | Type[BaseModel]) -> dict:
    if hasattr(model, '__subparserconfig__'):
        if isinstance(model.__subparserconfig__, SubparserConfig) is False:
            raise PydanticArgparseError("__subparserconfig__ must be an instance of SubparserConfig")
        parsms = model.__subparserconfig__.model_dump()
    else:
        parsms = {}
    return parsms
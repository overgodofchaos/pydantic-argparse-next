from argparse import ArgumentParser
from pydantic import BaseModel, Field
from typing import Type, Any, get_args, get_origin, Literal
import typing


class Argument(BaseModel):
    name: str = None
    alias: str | None = None
    required: bool | None = False
    positional: bool = False
    help: str | None = None
    type: Any = None
    default: Any = None
    nargs: int | str | None = None
    action: str | None = None
    choices: list[str] | None = None

    class Config:
        validate_assignment = True

    @property
    def names(self) -> list[str]:
        if self.alias:
            return [self.name, self.alias]
        return [self.name]

    def parametres(self):
        exclude = {
            "positional",
            "name",
            "alias"
        }

        if self.default is not None:
            self.required = False

        if self.positional:
            exclude.add("required")

            if self.required is False:
                self.nargs = "?"

        if self.action in ["store_true", "store_false"]:
            exclude.add("type")
            exclude.add("nargs")

        for key, value in self.model_dump().items():
            if value is None:
                exclude.add(key)

        params = self.model_dump(exclude=exclude)
        return params


class Extra(BaseModel):
    positional: bool = False

    class Config:
        validate_assignment = True

    # def __new__(cls, *args, **kwargs) -> dict:
    #     obj = super().__new__(cls, *args, **kwargs)
    #     obj.__init__()
    #     return obj.model_dump()


def parse(model: Type[BaseModel] | BaseModel, parser_=None) -> BaseModel:
    if parser_ is None:
        parser = ArgumentParser(
            prog="Program name",
            description="Program description",
            epilog="Program epilog"
        )
    else:
        parser = parser_

    subparsers = None

    fields = model.model_fields

    arguments = []

    for field in fields.keys():
        field_info = fields[field]

        if issubclass(field_info.annotation, BaseModel):
            if subparsers is None:
                subparsers = parser.add_subparsers()
            subparser = subparsers.add_parser(field)
            parse(field_info.annotation, subparser)
            continue



        argument = Argument()

        argument.name = field.replace("_", "-")

        if field_info.alias:
            argument.alias = field_info.alias.replace("_", "-")

        if field_info.default is not None:
            argument.required = False
            argument.default = field_info.default

        argument.type = field_info.annotation
        if str(argument.type).find("Optional") != -1:
            argument.type = get_args(field_info.annotation)[0]

        argument.help = field_info.description

        arguments.append(argument)

        if field_info.json_schema_extra:
            extra = Extra.model_validate(field_info.json_schema_extra)
        else:
            extra = Extra()

        if extra.positional is False:
            argument.positional = False
            argument.name = f"--{argument.name}"
            if argument.alias is not None:
                if argument.alias.startswith("-") is False:
                    argument.alias = f"--{argument.alias}"
        else:
            argument.positional = True

        if get_origin(argument.type) is not None:
            print(get_origin(field_info.annotation))
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

    print(arguments)
    for argument in arguments:
        print(argument)
        parser.add_argument(
            *argument.names,
            **argument.parametres()
        )

    if parser_ is None:
        args = parser.parse_args()
        return model.model_validate(args.__dict__)


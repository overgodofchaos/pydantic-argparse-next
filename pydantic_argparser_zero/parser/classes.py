from pydantic import BaseModel
from pydantic_core import PydanticUndefined
from typing import Any


# noinspection PyRedeclaration
class BaseModelArgsParser(BaseModel):
    class Config:
        validate_assignment = True


class ParserConfig(BaseModelArgsParser):
    prog: str | None = None
    usage: str | None = None
    description: str | None = None
    epilog: str | None = None
    argument_default: Any | None = None
    add_help: bool = True
    allow_abbrev: bool = True
    exit_on_error: bool = True


class SubparserConfig(BaseModelArgsParser):
    title: str = None
    description: str | None = None
    prog: str = None
    required: bool = True
    help: str | None = None


def subparserconfig(
        title: str | None = None,
        description: str | None = None,
        prog: str | None = None,
        required: bool = True,
        help: str | None = None,
):
    return SubparserConfig(title=title, description=description, prog=prog, required=required, help=help)


def parserconfig(
        prog: str = None,
        usage: str = None,
        description: str = None,
        epilog: str = None,
        argument_default: Any = None,
        add_help: bool = True,
        allow_abbrev: bool = True,
        exit_on_error: bool = True,
):
    return ParserConfig(prog=prog, usage=usage, description=description, epilog=epilog,
                        argument_default=argument_default, add_help=add_help,
                        allow_abbrev=allow_abbrev, exit_on_error=exit_on_error)


class Extra(BaseModelArgsParser):
    positional: bool = False


class Argument(BaseModelArgsParser):
    name: str = None
    alias: str | None = None
    required: bool | None = True
    positional: bool = False
    help: str | None = None
    type: Any = None
    default: Any = None
    nargs: int | str | None = None
    action: str | None = None
    choices: list[str] | None = None

    @property
    def names(self) -> list[str]:
        name = self.name.replace("_", "-")
        alias = self.alias.replace("_", "-") if self.alias else None
        if not self.positional:
            name = "--" + name
            if self.alias and alias.startswith("-") is False:
                alias = f"--{alias}"

        if self.alias:
            return [name, alias]
        return [name]

    def parametres(self):
        exclude = {
            "positional",
            "name",
            "alias"
        }

        if (self.default is not None and
                self.default is not PydanticUndefined):
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


class PydanticArgparseError(Exception):
    pass

from pydantic import BaseModel
from typing import Any


# noinspection PyRedeclaration
class BaseModelArgsParser(BaseModel):
    class Config:
        validate_assignment = True


class ParserConfig(BaseModelArgsParser):
    prog: str = None
    usage: str = None
    description: str = None
    epilog: str = None
    argument_default: Any = None
    add_help: bool = True
    allow_abbrev: bool = True
    exit_on_error: bool = True


class Extra(BaseModelArgsParser):
    positional: bool = False


class Argument(BaseModelArgsParser):
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


class PydanticArgparseError(Exception):
    pass

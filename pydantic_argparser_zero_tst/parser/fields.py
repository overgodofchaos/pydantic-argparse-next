import pydantic
from pydantic import types
# noinspection PyProtectedMember
from pydantic.fields import _Unset, FieldInfo, Deprecated, Any
# noinspection PyProtectedMember
from pydantic.fields import Callable, AliasPath, AliasChoices, PydanticUndefined
# noinspection PyProtectedMember
from pydantic.fields import JsonDict, Literal, Unpack, _EmptyKwargs
import typing
import annotated_types
from .classes import ExtraInfoArgument, ExtraInfoOption, ExtraInfoSubcommand


# noinspection PyPep8Naming,PyShadowingBuiltins
def Argument(
        default: Any = PydanticUndefined,
        *args,
        required: bool = True,
        default_factory: Callable[[], Any] | Callable[[dict[str, Any]], Any] | None = _Unset,
        alias: str | None = _Unset,
        alias_priority: int | None = _Unset,
        validation_alias: str | AliasPath | AliasChoices | None = _Unset,
        serialization_alias: str | None = _Unset,
        title: str | None = _Unset,
        field_title_generator: Callable[[str, FieldInfo], str] | None = _Unset,
        description: str | None = _Unset,
        examples: list[Any] | None = _Unset,
        exclude: bool | None = _Unset,
        discriminator: str | types.Discriminator | None = _Unset,
        deprecated: Deprecated | str | bool | None = _Unset,
        json_schema_extra: JsonDict | Callable[[JsonDict], None] | None = _Unset,
        frozen: bool | None = _Unset,
        validate_default: bool | None = _Unset,
        repr: bool = _Unset,
        init: bool | None = _Unset,
        init_var: bool | None = _Unset,
        kw_only: bool | None = _Unset,
        pattern: str | typing.Pattern[str] | None = _Unset,
        strict: bool | None = _Unset,
        coerce_numbers_to_str: bool | None = _Unset,
        gt: annotated_types.SupportsGt | None = _Unset,
        ge: annotated_types.SupportsGe | None = _Unset,
        lt: annotated_types.SupportsLt | None = _Unset,
        le: annotated_types.SupportsLe | None = _Unset,
        multiple_of: float | None = _Unset,
        allow_inf_nan: bool | None = _Unset,
        max_digits: int | None = _Unset,
        decimal_places: int | None = _Unset,
        min_length: int | None = _Unset,
        max_length: int | None = _Unset,
        union_mode: Literal['smart', 'left_to_right'] = _Unset,
        fail_fast: bool | None = _Unset,
        **extra: Unpack[_EmptyKwargs],
) -> Any:
    extra_info = ExtraInfoArgument(
        required=required,
    )

    if json_schema_extra is not None and json_schema_extra is not PydanticUndefined:
        json_schema_extra["pydantic_argparser_zero_extra"] = extra_info
    else:
        json_schema_extra = {
            "pydantic_argparser_zero_extra": extra_info,
        }

    # noinspection PyArgumentList
    return pydantic.Field(
        default,
        *args,
        default_factory=default_factory,
        alias=alias,
        alias_priority=alias_priority,
        validation_alias=validation_alias,
        serialization_alias=serialization_alias,
        title=title,
        field_title_generator=field_title_generator,
        description=description,
        examples=examples,
        exclude=exclude,
        discriminator=discriminator,
        deprecated=deprecated,
        json_schema_extra=json_schema_extra,
        coerce_numbers_to_str=coerce_numbers_to_str,
        gt=gt,
        ge=ge,
        lt=lt,
        le=le,
        multiple_of=multiple_of,
        allow_inf_nan=allow_inf_nan,
        max_digits=max_digits,
        decimal_places=decimal_places,
        min_length=min_length,
        max_length=max_length,
        union_mode=union_mode,
        fail_fast=fail_fast,
        **extra
    )


# noinspection PyPep8Naming,PyShadowingBuiltins
def Option(
        default: Any = PydanticUndefined,
        *args,
        required: bool = True,
        default_factory: Callable[[], Any] | Callable[[dict[str, Any]], Any] | None = _Unset,
        alias: str | None = _Unset,
        alias_priority: int | None = _Unset,
        validation_alias: str | AliasPath | AliasChoices | None = _Unset,
        serialization_alias: str | None = _Unset,
        title: str | None = _Unset,
        field_title_generator: Callable[[str, FieldInfo], str] | None = _Unset,
        description: str | None = _Unset,
        examples: list[Any] | None = _Unset,
        exclude: bool | None = _Unset,
        discriminator: str | types.Discriminator | None = _Unset,
        deprecated: Deprecated | str | bool | None = _Unset,
        json_schema_extra: JsonDict | Callable[[JsonDict], None] | None = _Unset,
        frozen: bool | None = _Unset,
        validate_default: bool | None = _Unset,
        repr: bool = _Unset,
        init: bool | None = _Unset,
        init_var: bool | None = _Unset,
        kw_only: bool | None = _Unset,
        pattern: str | typing.Pattern[str] | None = _Unset,
        strict: bool | None = _Unset,
        coerce_numbers_to_str: bool | None = _Unset,
        gt: annotated_types.SupportsGt | None = _Unset,
        ge: annotated_types.SupportsGe | None = _Unset,
        lt: annotated_types.SupportsLt | None = _Unset,
        le: annotated_types.SupportsLe | None = _Unset,
        multiple_of: float | None = _Unset,
        allow_inf_nan: bool | None = _Unset,
        max_digits: int | None = _Unset,
        decimal_places: int | None = _Unset,
        min_length: int | None = _Unset,
        max_length: int | None = _Unset,
        union_mode: Literal['smart', 'left_to_right'] = _Unset,
        fail_fast: bool | None = _Unset,
        **extra: Unpack[_EmptyKwargs],
) -> Any:
    extra_info = ExtraInfoOption(
        required=required,
    )

    if json_schema_extra is not None and json_schema_extra is not PydanticUndefined:
        json_schema_extra["pydantic_argparser_zero_extra"] = extra_info
    else:
        json_schema_extra = {
            "pydantic_argparser_zero_extra": extra_info,
        }

    # noinspection PyArgumentList
    return pydantic.Field(
        default,
        *args,
        default_factory=default_factory,
        alias=alias,
        alias_priority=alias_priority,
        validation_alias=validation_alias,
        serialization_alias=serialization_alias,
        title=title,
        field_title_generator=field_title_generator,
        description=description,
        examples=examples,
        exclude=exclude,
        discriminator=discriminator,
        deprecated=deprecated,
        json_schema_extra=json_schema_extra,
        coerce_numbers_to_str=coerce_numbers_to_str,
        gt=gt,
        ge=ge,
        lt=lt,
        le=le,
        multiple_of=multiple_of,
        allow_inf_nan=allow_inf_nan,
        max_digits=max_digits,
        decimal_places=decimal_places,
        min_length=min_length,
        max_length=max_length,
        union_mode=union_mode,
        fail_fast=fail_fast,
        **extra
    )


# noinspection PyPep8Naming,PyShadowingBuiltins
def Subcommand(
        default: Any = PydanticUndefined,
        *args,
        default_factory: Callable[[], Any] | Callable[[dict[str, Any]], Any] | None = _Unset,
        alias: str | None = _Unset,
        alias_priority: int | None = _Unset,
        validation_alias: str | AliasPath | AliasChoices | None = _Unset,
        serialization_alias: str | None = _Unset,
        title: str | None = _Unset,
        field_title_generator: Callable[[str, FieldInfo], str] | None = _Unset,
        description: str | None = _Unset,
        examples: list[Any] | None = _Unset,
        exclude: bool | None = _Unset,
        discriminator: str | types.Discriminator | None = _Unset,
        deprecated: Deprecated | str | bool | None = _Unset,
        json_schema_extra: JsonDict | Callable[[JsonDict], None] | None = _Unset,
        frozen: bool | None = _Unset,
        validate_default: bool | None = _Unset,
        repr: bool = _Unset,
        init: bool | None = _Unset,
        init_var: bool | None = _Unset,
        kw_only: bool | None = _Unset,
        pattern: str | typing.Pattern[str] | None = _Unset,
        strict: bool | None = _Unset,
        coerce_numbers_to_str: bool | None = _Unset,
        gt: annotated_types.SupportsGt | None = _Unset,
        ge: annotated_types.SupportsGe | None = _Unset,
        lt: annotated_types.SupportsLt | None = _Unset,
        le: annotated_types.SupportsLe | None = _Unset,
        multiple_of: float | None = _Unset,
        allow_inf_nan: bool | None = _Unset,
        max_digits: int | None = _Unset,
        decimal_places: int | None = _Unset,
        min_length: int | None = _Unset,
        max_length: int | None = _Unset,
        union_mode: Literal['smart', 'left_to_right'] = _Unset,
        fail_fast: bool | None = _Unset,
        **extra: Unpack[_EmptyKwargs],
) -> Any:
    extra_info = ExtraInfoSubcommand(
    )

    if json_schema_extra is not None and json_schema_extra is not PydanticUndefined:
        json_schema_extra["pydantic_argparser_zero_extra"] = extra_info
    else:
        json_schema_extra = {
            "pydantic_argparser_zero_extra": extra_info,
        }

    # noinspection PyArgumentList
    return pydantic.Field(
        default,
        *args,
        default_factory=default_factory,
        alias=alias,
        alias_priority=alias_priority,
        validation_alias=validation_alias,
        serialization_alias=serialization_alias,
        title=title,
        field_title_generator=field_title_generator,
        description=description,
        examples=examples,
        exclude=exclude,
        discriminator=discriminator,
        deprecated=deprecated,
        json_schema_extra=json_schema_extra,
        coerce_numbers_to_str=coerce_numbers_to_str,
        gt=gt,
        ge=ge,
        lt=lt,
        le=le,
        multiple_of=multiple_of,
        allow_inf_nan=allow_inf_nan,
        max_digits=max_digits,
        decimal_places=decimal_places,
        min_length=min_length,
        max_length=max_length,
        union_mode=union_mode,
        fail_fast=fail_fast,
        **extra
    )

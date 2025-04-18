import re

from ..testsimport import *


def test_store_true_true():
    class Temp(BaseModel):
        a: bool = pa.KwArg(False, description="temp")

    args = ["--a"]

    result = pa.parse(Temp, args=args)

    assert result.a is True


def test_store_true_true_2():
    class Temp(BaseModel):
        a: bool = pa.KwArg(False, description="temp", alias="-A")

    args = ["-A"]

    result = pa.parse(Temp, args=args)

    assert result.a is True


def test_store_true_false():
    class Temp(BaseModel):
        a: bool = pa.KwArg(False, description="temp")

    args = []

    result = pa.parse(Temp, args=args)

    assert result.a is False


def test_store_false_false():
    class Temp(BaseModel):
        a: bool = pa.KwArg(True, description="temp")

    args = ["--no-a"]

    result = pa.parse(Temp, args=args)

    assert result.a is False


def test_store_false_false_2():
    class Temp(BaseModel):
        a: bool = pa.KwArg(True, description="temp", alias="-A")

    args = ["--no-A"]

    result = pa.parse(Temp, args=args)

    assert result.a is False


def test_store_false_true():
    class Temp(BaseModel):
        a: bool = pa.KwArg(True, description="temp")

    args = []

    result = pa.parse(Temp, args=args)

    assert result.a is True


def test_store_required_error():
    class Temp(BaseModel):
        a: bool = pa.KwArg(..., description="temp")

    args = ["--a"]

    with pytest.raises(
        pa_classes.PydanticArgparserError,
        match="Boolean argument must have a default boolean value"
    ):
        result = pa.parse(Temp, args=args)


def test_store_positional_error():
    class Temp(BaseModel):
        a: bool = pa.Arg(False, description="temp")

    args = []

    with pytest.raises(
            pa_classes.PydanticArgparserError,
            match=re.escape("Positional argument can't be a boolean (store true or store false)")
    ):
        result = pa.parse(Temp, args=args)


def test_store_positional_error_2():
    class Temp(BaseModel):
        a: bool = pa.KwArg(..., description="temp")

    args = ["--a"]

    with pytest.raises(
            pa_classes.PydanticArgparserError,
            match=re.escape("Boolean argument must have a default boolean value"
                            " (False for store true or True for store false)")
    ):
        result = pa.parse(Temp, args=args)


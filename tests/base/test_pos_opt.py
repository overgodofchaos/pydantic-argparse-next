from ..testsimport import *


def test_argument_positional_optional():
    class Temp(BaseModel):
        a: str = pa.Arg(None, description="temp")

    args = ["test"]

    result = pa.parse(
        model=Temp,
        args=args,
    )

    assert result.a == "test"


def test_argument_positional_optional_not_defined():
    class Temp(BaseModel):
        a: str = pa.Arg(None, description="temp")

    args = []

    result = pa.parse(
        model=Temp,
        args=args,
    )

    assert result.a is None


def test_argument_positional_optional_not_defined_2():
    class Temp(BaseModel):
        a: Optional[str] = pa.Arg(..., description="temp")

    args = []

    result = pa.parse(
        model=Temp,
        args=args,
    )

    assert result.a is None


def test_argument_positional_optional_not_defined_3():
    class Temp(BaseModel):
        a: Union[str, None] = pa.Arg(..., description="temp")

    args = []

    result = pa.parse(
        model=Temp,
        args=args,
    )

    assert result.a is None


def test_argument_positional_optional_not_defined_4():
    class Temp(BaseModel):
        a: Optional[str] = pa.Arg(None, description="temp")

    args = []

    result = pa.parse(
        model=Temp,
        args=args,
    )

    assert result.a is None




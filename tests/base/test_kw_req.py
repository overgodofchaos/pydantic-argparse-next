from ..testsimport import *


def test_argument_keyword_required():
    class Temp(BaseModel):
        a: str = pa.KwArg(..., description="temp")

    args = ["--a", "test"]

    result = pa.parse(
        model=Temp,
        args=args,
    )

    assert result.a == "test"


def test_argument_keyword_required_2():
    class Temp(BaseModel):
        a: str = pa.KwArg(..., description="temp", alias="A")

    args = ["--A", "test"]

    result = pa.parse(
        model=Temp,
        args=args,
    )

    assert result.a == "test"


def test_argument_keyword_required_3():
    class Temp(BaseModel):
        a: str = pa.KwArg(..., description="temp", alias="-A")

    args = ["-A", "test"]

    result = pa.parse(
        model=Temp,
        args=args,
    )

    assert result.a == "test"


def test_argument_keyword_required_4():
    class Temp(BaseModel):
        a: str = Field(..., description="temp")

    args = ["--a", "test"]

    result = pa.parse(
        model=Temp,
        args=args,
    )

    assert result.a == "test"


def test_argument_keyword_required_not_found_error():
    class Temp(BaseModel):
        a: str = pa.KwArg(..., description="temp")

    args = []

    with pytest.raises(
        pa_classes.PydanticArgparserError,
        match="Keyword argument --a is required"
    ):
        result = pa.parse(
            model=Temp,
            args=args,
        )

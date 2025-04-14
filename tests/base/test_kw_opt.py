from ..testsimport import *


def test_argument_keyword_optional():
    class Temp(BaseModel):
        a: str = pa.KwArg(None, description="temp")

    args = ["--a", "test"]

    result = pa.parse(
        model=Temp,
        args=args,
    )

    assert result.a == "test"


def test_argument_keyword_optional_2():
    class Temp(BaseModel):
        a: str = pa.KwArg(None, description="temp", alias="A")

    args = ["--A", "test"]

    result = pa.parse(
        model=Temp,
        args=args,
    )

    assert result.a == "test"


def test_argument_keyword_optional_3():
    class Temp(BaseModel):
        a: str = pa.KwArg(None, description="temp", alias="-A")

    args = ["-A", "test"]

    result = pa.parse(
        model=Temp,
        args=args,
    )

    assert result.a == "test"


def test_argument_keyword_optional_4():
    class Temp(BaseModel):
        a: str = Field(None, description="temp")

    args = ["--a", "test"]

    result = pa.parse(
        model=Temp,
        args=args,
    )

    assert result.a == "test"


def test_argument_keyword_optional_not_defined():
    class Temp(BaseModel):
        a: str = pa.KwArg(None, description="temp")

    args = []

    result = pa.parse(
        model=Temp,
        args=args,
    )

    

    assert result.a is None


def test_argument_keyword_optional_not_defined_2():
    class Temp(BaseModel):
        a: Optional[str] = pa.KwArg(..., description="temp")

    args = []

    result = pa.parse(
        model=Temp,
        args=args,
    )

    

    assert result.a is None


def test_argument_keyword_optional_not_defined_3():
    class Temp(BaseModel):
        a: Union[str | None] = pa.KwArg(..., description="temp")

    args = []

    result = pa.parse(
        model=Temp,
        args=args,
    )

    

    assert result.a is None


def test_argument_keyword_optional_not_defined_4():
    class Temp(BaseModel):
        a: Union[str | None] = pa.KwArg(None, description="temp")

    args = []

    result = pa.parse(
        model=Temp,
        args=args,
    )

    assert result.a is None



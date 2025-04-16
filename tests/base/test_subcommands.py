import pytest

from ..testsimport import *


@pytest.fixture
def config_model():
    class SubCommand1(BaseModel):
        c: str = pa.Arg(..., description="test")
        d: str = pa.KwArg(..., description="test")

    class SubCommand2(BaseModel):
        e: str = pa.Arg(..., description="test")
        f: str = pa.KwArg(..., description="test")

    class Temp(BaseModel):
        a: str = pa.Arg(..., description="temp")
        b: str = pa.KwArg(None, description="test")

        subcommand1: Optional[SubCommand1] = pa.Subcommand(..., description="test")
        subcommand2: Optional[SubCommand2] = pa.Subcommand(..., description="test")

    return Temp


@pytest.fixture
def config_model_2():
    class SubCommand1(BaseModel):
        c: str = pa.Arg(..., description="test")
        d: str = pa.KwArg(..., description="test")

    class SubCommand2(BaseModel):
        e: str = pa.Arg(..., description="test")
        f: str = pa.KwArg(..., description="test")

    class Temp(BaseModel):
        a: str = pa.Arg(..., description="temp")
        b: str = pa.KwArg(None, description="test")

        subcommand1: SubCommand1 = pa.Subcommand(None, description="test")
        subcommand2: SubCommand2 = pa.Subcommand(None, description="test")

    return Temp


def test_argument_subcommand(config_model):
    model = config_model

    args = [
        "test",
        "--b", "test2",
        "subcommand1",
        "test3",
        "--d", "test4",
    ]

    result = pa.parse(
        model=model,
        args=args,
    )

    assert result.a == "test"
    assert result.b == "test2"
    assert result.subcommand1.c == "test3"
    assert result.subcommand1.d == "test4"
    assert result.subcommand2 is None
    assert result.__subcommand__.name == "subcommand1"
    assert result.__subcommand__.value.c == "test3"
    assert result.__subcommand__.value.d == "test4"


def test_argument_subcommand_not_defined(config_model):
    model = config_model

    args = [
        "test",
        "--b", "test2"
    ]

    with pytest.raises(
        pa_classes.PydanticArgparserError,
        match="Subcommand required"
    ):
        result = pa.parse(
            model=model,
            args=args,
        )


def test_argument_subcommand_not_defined_2(config_model):
    model = config_model

    model.__parserconfig__ = pa.parserconfig(
        subcommand_required=False
    )

    args = [
        "test",
        "--b", "test2"
    ]

    result = pa.parse(
        model=model,
        args=args,
    )

    assert result.a == "test"
    assert result.b == "test2"
    assert result.subcommand1 is None
    assert result.subcommand2 is None


def test_argument_subcommand_not_defined_3(config_model_2):
    model = config_model_2

    model.__parserconfig__ = pa.parserconfig(
        subcommand_required=False
    )

    args = [
        "test",
        "--b", "test2"
    ]

    result = pa.parse(
        model=model,
        args=args,
    )

    assert result.a == "test"
    assert result.b == "test2"
    assert result.subcommand1 is None
    assert result.subcommand2 is None





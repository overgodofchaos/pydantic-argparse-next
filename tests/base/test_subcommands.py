from ..testsimport import *


def test_argument_subcommand():
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

    args = [
        "test",
        "--b", "test2",
        "subcommand1",
        "test3",
        "--d", "test4",
    ]

    result = pa.parse(
        model=Temp,
        args=args,
    )

    assert result.a == "test"
    assert result.b == "test2"
    assert result.subcommand1.c == "test3"
    assert result.subcommand1.d == "test4"



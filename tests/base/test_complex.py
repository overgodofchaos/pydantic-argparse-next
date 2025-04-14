from ..testsimport import *


def test_complex():
    class Choices(Enum):
        choice1 = 0
        choice2 = 1

    class SubCommand1(BaseModel):
        k: str = pa.KwArg("test", description="test")

    class SubCommand2(BaseModel):
        l: str = pa.KwArg("test", description="test")

    class Test(BaseModel):
        a: str = pa.Arg(..., description="test")
        b: str = pa.Arg(None, description="test")
        c: str = pa.KwArg(..., description="test")
        d: str = pa.KwArg(None, description="test")
        e: bool = pa.KwArg(False, description="test")
        f: bool = pa.KwArg(True, description="test")
        g: Literal["choice1", "choice2"] = pa.KwArg(..., description="test")
        h: Choices = pa.KwArg(Choices.choice1, description="test")
        i: Optional[SubCommand1] = pa.Subcommand(..., description="test")
        j: Optional[SubCommand1] = pa.Subcommand(..., description="test")

    args = [
        "test_a",
        "--c", "test_c",
        "--e",
        "--no-f",
        "--g", "choice1",
        "--h", "choice2",
        "i",
        "--k", "test_k"
    ]

    result = pa.parse(Test, args)

    assert result.a == "test_a"
    assert result.b is None
    assert result.c == "test_c"
    assert result.d is None
    assert result.e is True
    assert result.f is False
    assert result.g == "choice1"
    assert result.h is Choices.choice2
    assert isinstance(result.i, SubCommand1)
    assert result.j is None
    assert result.i.k == "test_k"
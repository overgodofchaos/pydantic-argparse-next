from ..testsimport import *

#
# def test_test(capsys):
#     class Test(BaseModel):
#         a: str = pa.KwArg(..., description="test")
#
#     args = ["--help"]
#
#     with patch("sys.exit") as mocked_exit:
#         result = pa.parse(Test, args)
#         mocked_exit.assert_called_once()
#
#     captured = capsys.readouterr()


def test_help(capsys):
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
        g: Literal["test1", "test2"] = pa.KwArg(..., description="test")
        h: Choices = pa.KwArg(Choices.choice1, description="test")
        i: Optional[SubCommand1] = pa.Subcommand(..., description="test")
        j: Optional[SubCommand1] = pa.Subcommand(..., description="test")

    args = ["--help"]

    with pytest.raises(SystemExit) as exc_info:
        pa.parse(Test, args)

    assert exc_info.value.code == 0

from ..testsimport import *


log = logger.get_logger("test_help")


def read_output(model, args, capsys):
    with patch("sys.exit") as mocked_exit:
        result = pa.parse(model, args=args)
        # mocked_exit.assert_called_once()

    return capsys.readouterr()


def test_help_general():
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
        pa.parse(Test, args=args)

    assert exc_info.value.code == 0


def test_help_general_2(capsys):
    class Test(BaseModel):
        a: str = pa.KwArg(..., description="test")
        b: str = pa.KwArg(None, description="test")

    output = read_output(Test, ["--help"], capsys).out

    assert "--help (-H)" in output
    assert "Show this message and exit." in output


def test_parserconfig(capsys):
    class Test(BaseModel):
        __parserconfig__ = pa.parserconfig(
            program_name="Test program name",
            description="Test program description",
            epilog="Test program epilog",
            version="1.0.5"
        )

        a: str = pa.KwArg(..., description="test")
        b: str = pa.KwArg(None, description="test")

    output = read_output(Test, ["--help"], capsys).out

    assert "Test program name" in output
    assert "Test program description" in output
    assert "Test program epilog" in output
    assert "1.0.5" in output


def test_parserconfig_2(capsys):
    class Test(BaseModel):
        a: str = pa.KwArg(..., description="test")
        b: str = pa.KwArg(None, description="test")

    with patch("sys.exit") as mocked_exit:
        result = pa.parse(
            Test,
            args=["--help"],
            program_name="Test program name",
            description="Test program description",
            epilog="Test program epilog",
            version="1.0.5"
        )

    output = capsys.readouterr().out

    assert "Test program name" in output
    assert "Test program description" in output
    assert "Test program epilog" in output
    assert "1.0.5" in output


def test_help_subcomands(capsys):
    class SubSubCommand1(BaseModel):
        __parserconfig__ = pa.parserconfig(
            program_name="SS1-N",
            description="SS1-D",
            epilog="SS1-E",
        )
        h: str = pa.KwArg("test", description="test")

    class SubSubCommand2(BaseModel):
        __parserconfig__ = pa.parserconfig(
            program_name="SS2-N",
            description="SS2-D",
            epilog="SS2-E",
        )
        i: str = pa.KwArg("test", description="test")

    class SubCommand1(BaseModel):
        __parserconfig__ = pa.parserconfig(
            program_name="S1-N",
            description="S1-D",
            epilog="S1-E",
        )
        d: str = pa.KwArg("test", description="test")
        e: Optional[SubSubCommand1] = pa.Subcommand(..., description="test")
        f: Optional[SubSubCommand2] = pa.Subcommand(..., description="test")

    class SubCommand2(BaseModel):
        __parserconfig__ = pa.parserconfig(
            program_name="S2-N",
            description="S2-D",
            epilog="S2-E",
        )
        g: str = pa.KwArg("test", description="test")

    class Test(BaseModel):
        a: str = pa.Arg(None, description="test")
        b: Optional[SubCommand1] = pa.Subcommand(..., description="test")
        c: Optional[SubCommand1] = pa.Subcommand(..., description="test")

    args = [
        "b",
        "--help"
    ]

    output = read_output(Test, args, capsys).out

    assert "pytest b" in output
    assert "S1-N" not in output
    assert "S1-D" in output
    assert "S1-E" in output

    args = [
        "b",
        "e",
        "--help"
    ]

    output = read_output(Test, args, capsys).out

    assert "pytest b e" in output
    assert "SS1-N" not in output
    assert "SS1-D" in output
    assert "SS1-E" in output


def test_help_subcomands_2(capsys):

    class SubCommand1(BaseModel):
        d: str = pa.KwArg("test", description="test")

    class SubCommand2(BaseModel):
        e: str = pa.KwArg("test", description="test")

    class Test(BaseModel):
        a: str = pa.Arg(None, description="test")
        b: Optional[SubCommand1] = pa.Subcommand(
            ...,
            description="test",
            long_description="S1-D",
            epilog="S1-E",
        )
        c: Optional[SubCommand1] = pa.Subcommand(
            ...,
            description="test",
            long_description="S2-D",
            epilog="S2-E",
        )

    args = [
        "b",
        "--help"
    ]

    output = read_output(Test, args, capsys).out

    assert "pytest b" in output
    assert "S1-D" in output
    assert "S1-E" in output


def test_help_variadic(capsys):
    class Test(BaseModel):
        a: list[str]
        b: tuple[str, int, float]
        c: tuple
        d: list[int] = pa.KwArg(n_args="2...6")
        e: list[str] = pa.KwArg(n_args="2...3")

    output = read_output(Test, ["--help"], capsys).out

    assert "LIST[STR] (arg1, {arg2, ...})" in output
    assert "TUPLE (arg1 STR, arg2 INT, arg3 FLOAT)" in output
    assert "TUPLE[STR] (arg1, {arg2, ...})" in output
    assert "LIST[INT] (arg1, arg2, {arg3, ..., arg6})" in output
    assert "LIST[STR] (arg1, arg2, {arg3})" in output


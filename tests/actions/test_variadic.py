from ..testsimport import *
from pathlib import Path


def test_variadic_list():
    class Temp(BaseModel):
        a: list[str]
        b: list[int]
        c: list
        d: typing.List
        e: list = pa.KwArg(n_args="2...4")

    args = [
        "--a", "one", "two", "three",
        "--b", "1", "2", "3",
        "--c", "one", "two", "three",
        "--d", "one", "two", "three",
        "--e", "one", "two", "three",
    ]

    result = pa.parse(Temp, args=args)

    assert result.a[1] == "two"
    assert result.b[1] == 2
    assert result.c[1] == "two"
    assert result.d[1] == "two"
    assert result.e[1] == "two"


def test_variadic_list_too_many_args():
    class Temp(BaseModel):
        a: list[str] = pa.KwArg(n_args="1...3")

    args = [
        "--a", "one", "2", "three", "4"
    ]

    with pytest.raises(
        pa_classes.PydanticArgparserError,
        match="Argument number of arguments for --a must be between 1 and 3. But got 4."
    ):
        result = pa.parse(Temp, args=args)


def test_variadic_list_too_few_args():
    class Temp(BaseModel):
        a: list[str] = pa.KwArg(n_args="3...5")

    args = [
        "--a", "one", "2"
    ]

    with pytest.raises(
        pa_classes.PydanticArgparserError,
        match="Argument number of arguments for --a must be between 3 and 5. But got 2."
    ):
        result = pa.parse(Temp, args=args)


def test_variadic_tuple():
    class Temp(BaseModel):
        a: tuple[str, int, Path]
        b: tuple

    args = [
        "--a", "one", "2", "three",
        "--b", "one", "2", "three", "4",
    ]

    result = pa.parse(Temp, args=args)

    assert result.a[0] == "one"
    assert result.a[1] == 2
    assert isinstance(result.a[2], Path)
    assert result.b[0] == "one"
    assert result.b[1] == "2"


def test_variadic_tuple_too_many_args():
    class Temp(BaseModel):
        a: tuple[str, int, Path]

    args = [
        "--a", "one", "2", "three", "4"
    ]

    with pytest.raises(
        pa_classes.PydanticArgparserError,
        match="Argument number of arguments for --a must be 3. But got 4."
    ):
        result = pa.parse(Temp, args=args)


def test_variadic_tuple_too_few_args():
    class Temp(BaseModel):
        a: tuple[str, int, Path]

    args = [
        "--a", "one", "2"
    ]

    with pytest.raises(
        pa_classes.PydanticArgparserError,
        match=re.escape("Argument number of arguments for --a must be 3. But got 2.")
    ):
        result = pa.parse(Temp, args=args)


def test_variadic_positional():
    class Temp(BaseModel):
        a: list[str] = pa.Arg(n_args=3)
        b: tuple[str, str, str] = pa.Arg()

    args = [
        "one", "two", "three",
        "one", "two", "three",
    ]

    result = pa.parse(Temp, args=args)

    assert result.a[1] == "two"
    assert result.b[1] == "two"


def test_variadic_positional_error():
    class Temp(BaseModel):
        a: list[str] = pa.Arg(n_args="2...4")

    args = [
        "one", "two", "three",
    ]

    with pytest.raises(
        pa_classes.PydanticArgparserError,
        match="A positional variadic argument must have a strictly defined number of arguments. But 2...4 was given."
    ):
        result = pa.parse(Temp, args=args)


def test_variadic_incorrect_n_args_error():
    class Temp(BaseModel):
        a: list[str] = pa.KwArg(n_args="4...2")

    args = [
        "--a", "one", "two", "three",
    ]

    with pytest.raises(
        pa_classes.PydanticArgparserError,
        match="Maximum number of arguments should be greater than minimum. But 4...2 was given."
    ):
        result = pa.parse(Temp, args=args)


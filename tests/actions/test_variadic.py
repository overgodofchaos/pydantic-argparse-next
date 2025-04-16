from ..testsimport import *
from pathlib import Path


def test_variadic_list():
    class Temp(BaseModel):
        a: list[str]
        b: list[int]

    args = [
        "--a", "one", "two", "three",
        "--b", "1", "2", "3"
    ]

    result = pa.parse(Temp, args=args)

    assert result.a[1] == "two"
    assert result.b[1] == 2


def test_variadic_tuple():
    class Temp(BaseModel):
        a: tuple[str, int, Path]

    args = [
        "--a", "one", "2", "three",
    ]

    result = pa.parse(Temp, args=args)

    assert result.a[0] == "one"
    assert result.a[1] == 2
    assert isinstance(result.a[2], Path)


def test_variadic_tuple_too_many_args():
    class Temp(BaseModel):
        a: tuple[str, int, Path]

    args = [
        "--a", "one", "2", "three", "4"
    ]

    with pytest.raises(
        pa_classes.PydanticArgparserError,
        match="Argument number of arguments for --a must be between 3 and  3. But got 4."
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
        match=re.escape("Argument number of arguments for --a must be between 3 and  3. But got 2.")
    ):
        result = pa.parse(Temp, args=args)
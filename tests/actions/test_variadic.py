import pydantic_argparse_next as pa
from pydantic import BaseModel


def test_variadic_list():
    class Temp(BaseModel):
        a: list[str]
        b: list[int]

    args = [
        "--a", "one", "two", "three",
        "--b", "1", "2", "3"
    ]

    result = pa.parse(Temp)

    assert result.a[1] == "two"
    assert result.b[1] == 2
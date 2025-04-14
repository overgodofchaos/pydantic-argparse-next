from pydantic_argparse_new.parser.classes import PydanticArgparserError
from ..testsimport import *


def test_argument_keyword_not_exist_argument():
    class Temp(BaseModel):
        a: str = pa.KwArg(None, description="temp")

    args = [
        "--a", "test",
        "--b", "test2",
    ]

    with pytest.raises(
        pa_classes.PydanticArgparserError,
        match="Unrecognized argument: --b"
    ):
        result = pa.parse(
            model=Temp,
            args=args,
        )




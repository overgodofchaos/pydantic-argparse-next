from ..testsimport import *


def test_argument_positional_required():
    class Temp(BaseModel):
        a: str = pa.Arg(..., description="temp")

    args = ["test"]

    result = pa.parse(
        model=Temp,
        args=args,
    )

    

    assert result.a == "test"


def test_argument_positional_required_not_found_error():
    class Temp(BaseModel):
        a: str = pa.Arg(..., description="temp")

    args = []

    with pytest.raises(
        pa_classes.PydanticArgparserError,
        match="Argument a is required"
    ):
        result = pa.parse(
            model=Temp,
            args=args,
        )

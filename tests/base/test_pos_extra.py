from ..testsimport import *


def test_argument_positional_required_excess_argument():
    class Temp(BaseModel):
        a: str = pa.Arg(..., description="temp")

    args = ["test", "test2"]


    with pytest.raises(
        pa_classes.PydanticArgparserError,
        match="Argument test2 is not defined"
    ):
        result = pa.parse(
            model=Temp,
            args=args,
        )

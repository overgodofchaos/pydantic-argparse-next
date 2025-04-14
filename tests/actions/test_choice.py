import pytest

from ..testsimport import *


def test_choice():
    class Test(BaseModel):
        a: Literal["choice1", "choice2"] = pa.Arg(..., description="test")

    args = ["choice1"]

    result = pa.parse(Test, args)

    assert result.a == "choice1"


def test_choice_2():
    class Test(BaseModel):
        a: Literal["choice1", "choice2"] = pa.Arg("choice2", description="test")

    args = []

    result = pa.parse(Test, args)

    assert result.a == "choice2"


def test_choice_3():
    class Test(BaseModel):
        a: Literal["choice1", "choice2"] = pa.Arg(..., description="test")

    args = ["choice3"]

    with pytest.raises(
        ValidationError,
        match=r".*Input should be 'choice1' or 'choice2'.*"
    ):
        result = pa.parse(Test, args)


def test_choice_4():
    class Choices(Enum):
        choice1 = 1
        choice2 = 2

    class Test(BaseModel):
        a: Choices = pa.Arg(..., description="test")

    args = ["choice1"]

    result = pa.parse(Test, args)

    assert result.a is Choices.choice1


def test_choice_5():
    class Choices(Enum):
        choice1 = 1
        choice2 = 2

    class Test(BaseModel):
        a: Choices = pa.Arg(Choices.choice2, description="test")

    args = []

    result = pa.parse(Test, args)

    assert result.a is Choices.choice2


def test_choice_6():
    class Choices(Enum):
        choice1 = 1
        choice2 = 2

    class Test(BaseModel):
        a: Choices = pa.Arg(..., description="test")

    args = ["choice3"]

    with pytest.raises(
        pa_classes.PydanticArgparserError,
        match=re.escape("Input should be in [choice1, choice2] for a, but choice3 was given")
    ):
        result = pa.parse(Test, args)


def test_choice_7():
    class Test(BaseModel):
        a: Literal["choice1", "choice2"] = pa.KwArg(..., description="test")

    args = ["--a", "choice1"]

    result = pa.parse(Test, args)

    assert result.a == "choice1"
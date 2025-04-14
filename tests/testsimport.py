import pydantic_argparse_new as pa
from pydantic_argparse_new.parser import classes as pa_classes
from pydantic import BaseModel, Field, ValidationError
from typing import Optional, Union, Literal
from enum import Enum
import pytest
import re
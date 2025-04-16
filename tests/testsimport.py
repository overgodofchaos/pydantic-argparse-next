import pydantic_argparse_next as pa
from pydantic_argparse_next.parser import classes as pa_classes
from pydantic import BaseModel, Field, ValidationError
from typing import Optional, Union, Literal
from enum import Enum
import pytest
import re
from unittest.mock import patch
from mx_logger import logger

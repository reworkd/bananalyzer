from typing import Optional

from pydantic import BaseModel, Field

from bananalyzer.data.schemas import GoalType


class PytestArgs(BaseModel):
    s: bool
    n: Optional[int]


class Args(BaseModel):
    path: str
    headless: bool
    id: Optional[str] = Field(default=None)
    intent: Optional[GoalType] = Field(default=None)
    domain: Optional[str] = Field(default=None)
    pytest_args: PytestArgs

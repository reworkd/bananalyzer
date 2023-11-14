from typing import Optional

from pydantic import BaseModel, Field

from bananalyzer import GoalType


class Args(BaseModel):
    path: str
    headless: bool
    id: Optional[str] = Field(default=None)
    intent: Optional[GoalType] = Field(default=None)
    domain: Optional[str] = Field(default=None)
    s: bool

from typing import Optional

from pydantic import BaseModel, Field

from bananalyzer import GoalType


class Args(BaseModel):
    path: str
    headless: bool
    intent: Optional[GoalType] = Field(default=None)
    id: Optional[str] = Field(default=None)

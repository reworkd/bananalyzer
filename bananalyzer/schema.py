from typing import List, Optional

from pydantic import BaseModel, Field

from bananalyzer.data.schemas import GoalType


class PytestArgs(BaseModel):
    s: bool
    n: Optional[int]
    q: bool


class Args(BaseModel):
    path: str
    headless: bool
    single_browser_instance: bool
    id: Optional[str] = Field(default=None)
    intent: Optional[GoalType] = Field(default=None)
    domain: Optional[str] = Field(default=None)
    subdomain: Optional[str] = Field(default=None)
    skip: List[str]
    type: Optional[str] = Field(default=None)
    download: bool
    test: bool
    pytest_args: PytestArgs


class AgentRunnerClass(BaseModel):
    class_name: str
    class_path: str

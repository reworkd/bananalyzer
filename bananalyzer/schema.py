from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

from bananalyzer.data.schemas import GoalType


class PytestArgs(BaseModel):
    s: bool
    n: Optional[int]
    q: bool
    xml: Optional[str]


class Args(BaseModel):
    path: Union[str, Literal["DOWNLOAD_ONLY"]]
    headless: bool
    single_browser_instance: bool
    id: Optional[str] = Field(default=None)
    domain: Optional[str] = Field(default=None)
    intent: Optional[GoalType] = Field(default=None)
    category: Optional[str] = Field(default=None)
    subcategory: Optional[str] = Field(default=None)
    skip: List[str]
    type: Optional[str] = Field(default=None)
    download: bool
    test: bool
    count: Optional[int]
    pytest_args: PytestArgs


class AgentRunnerClass(BaseModel):
    class_name: str
    class_path: str


MARKER_PREFIX = "bananalyzer_"

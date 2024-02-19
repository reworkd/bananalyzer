from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

from bananalyzer.data.schemas import GoalType

XDistDistributionMode = Literal[
    "load", "loadscope", "loadfile", "loadgroup", "worksteal", "no"
]


class PytestArgs(BaseModel):
    s: bool
    q: bool
    xml: Optional[str] = Field(description="Path to the xml report file")


class XDistArgs(BaseModel):
    dist: XDistDistributionMode = Field(description="Distribution mode (xdist)")
    n: Union[int, Literal["logical", "auto"]] = Field(
        description="Number of workers (xdist)"
    )


class Args(BaseModel):
    path: Union[str, Literal["DOWNLOAD_ONLY"]]
    headless: bool
    single_browser_instance: bool
    id: Optional[List[str]] = Field(default=None)
    tags: Optional[List[str]] = Field(default=None)
    domain: Optional[str] = Field(default=None)
    intent: Optional[GoalType] = Field(default=None)
    category: Optional[str] = Field(default=None)
    subcategory: Optional[str] = Field(default=None)
    skip: List[str]
    type: Optional[str] = Field(default=None)
    download: bool
    examples_bucket: Optional[str] = Field(default=None)
    test: bool
    count: Optional[int]
    pytest_args: PytestArgs
    xdist_args: XDistArgs


class AgentRunnerClass(BaseModel):
    class_name: str
    class_path: str


MARKER_PREFIX = "bananalyzer_"

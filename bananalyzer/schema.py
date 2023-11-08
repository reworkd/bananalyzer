from pydantic import BaseModel


class Args(BaseModel):
    path: str
    headless: bool

from typing import Literal
from pydantic import BaseModel


class ProjectSpec(BaseModel):
    project_title: str
    project_type: Literal["bot", "api"]

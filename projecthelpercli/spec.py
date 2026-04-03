from typing import Literal

from pydantic import BaseModel, model_validator

FeatureName = Literal["git", "uv", "uv-no-git", "pytest", "ruff", "mypy"]


class ProjectSpec(BaseModel):
    project_title: str
    project_type: Literal["bot", "api"]
    project_description: str | None = None
    project_version: str = "1.0.0"
    features: list[FeatureName] = []

    @model_validator(mode="after")
    def check_uv_conflict(self) -> "ProjectSpec":
        if "uv" in self.features and "uv-no-git" in self.features:
            raise ValueError("'uv' and 'uv-no-git' are mutually exclusive")
        return self

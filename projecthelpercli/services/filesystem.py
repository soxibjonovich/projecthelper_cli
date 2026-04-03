from projecthelpercli.spec import ProjectSpec
from pathlib import Path


def create_project_dir(spec: ProjectSpec) -> Path:
    project_dir = Path.cwd() / spec.project_title

    if project_dir.exists():
        raise FileExistsError(f"Folder '{spec.project_title}' already exists.")

    project_dir.mkdir()
    return project_dir

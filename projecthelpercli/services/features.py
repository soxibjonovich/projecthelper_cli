import subprocess
from pathlib import Path

from projecthelpercli.spec import ProjectSpec


def execute_features(project_directory: Path, spec: ProjectSpec):
    for feature in spec.features:
        match feature:
            case "git":
                _init_git(project_directory)
            case "uv":
                _init_uv(project_directory)
            case "uv-no-git":
                _init_uv(project_directory, no_git=True)
            case "pytest":
                _add_dev_dep(project_directory, "pytest")
            case "ruff":
                _add_dev_dep(project_directory, "ruff")
            case "mypy":
                _add_dev_dep(project_directory, "mypy")


def _init_git(directory: Path):
    subprocess.run(["git", "init"], cwd=directory, check=True, capture_output=True)


def _init_uv(directory: Path, no_git: bool = False):
    cmd = ["uv", "init", "--no-vcs"] if no_git else ["uv", "init"]
    subprocess.run(cmd, cwd=directory, check=True, capture_output=True)


def _add_dev_dep(directory: Path, package: str):
    subprocess.run(
        ["uv", "add", "--dev", package],
        cwd=directory,
        check=True,
        capture_output=True,
    )

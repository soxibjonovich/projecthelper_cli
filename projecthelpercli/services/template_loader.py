import pathlib

BUILTIN_TEMPLATES = pathlib.Path(__file__).parent.parent / "templates"
USER_TEMPLATES = pathlib.Path.home() / ".projecthelpercli" / "templates"


def find_template_dir(project_type: str) -> pathlib.Path:
    user_path = USER_TEMPLATES / project_type
    if user_path.exists():
        return user_path
    return BUILTIN_TEMPLATES / project_type


def check_templates() -> bool:
    return USER_TEMPLATES.exists() and any(USER_TEMPLATES.iterdir())

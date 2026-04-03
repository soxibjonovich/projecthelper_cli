from pathlib import Path
import jinja2

from projecthelpercli.spec import ProjectSpec
from projecthelpercli.services.template_loader import find_template_dir


def render_templates(spec: ProjectSpec, project_dir: Path) -> list[Path]:
    template_dir = find_template_dir(spec.project_type)
    loader = jinja2.FileSystemLoader(str(template_dir))
    env = jinja2.Environment(loader=loader)

    created = []
    for template_file in template_dir.iterdir():
        template = env.get_template(template_file.name)
        content = template.render(project_title=spec.project_title)

        output_file = project_dir / template_file.name.replace(".j2", "")
        output_file.write_text(content)
        created.append(output_file)

    return created

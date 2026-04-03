from pathlib import Path

import jinja2

from projecthelpercli.services.template_loader import find_template_dir
from projecthelpercli.spec import ProjectSpec


def render_templates(spec: ProjectSpec, project_dir: Path) -> list[Path]:
    template_dir = find_template_dir(spec.project_type)
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(str(template_dir)))

    created = []
    for template_file in template_dir.rglob("*.j2"):
        relative = template_file.relative_to(template_dir)
        output_path = project_dir / str(relative).removesuffix(".j2")

        output_path.parent.mkdir(parents=True, exist_ok=True)

        template = env.get_template(str(relative))
        content = template.render(spec=spec)
        output_path.write_text(content)
        created.append(output_path)

    return created

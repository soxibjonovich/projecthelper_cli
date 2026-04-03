from typing import Annotated, Literal

import typer
from rich.console import Console

from projecthelpercli.services import filesystem, renderer, template_loader
from projecthelpercli.spec import ProjectSpec

app = typer.Typer()
console = Console()
err_console = Console(stderr=True)


@app.command()
def init(
    project_type: Annotated[Literal["bot", "api"], typer.Argument(help="Project type")],
    project_title: Annotated[str, typer.Argument(help="Project title")],
    project_description: Annotated[
        str | None, typer.Option("--description", "-d", help="Project description")
    ] = None,
    project_version: Annotated[
        str, typer.Option("--version", "-v", help="Project version", min=1)
    ] = "1.0.0",
):
    spec = ProjectSpec(
        project_title=project_title,
        project_type=project_type,
        project_description=project_description,
        project_version=project_version,
    )

    try:
        project_dir = filesystem.create_project_dir(spec)
    except FileExistsError as e:
        err_console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)

    created = renderer.render_templates(spec, project_dir)
    for path in created:
        console.print(f"  [dim]→[/dim] {path.name}")

    console.print(f"\n[green]✓[/green] [bold]'{spec.project_title}'[/bold] created.")


@app.command()
def validate():
    if template_loader.check_templates():
        console.print("[green]✓ Custom templates found.[/green]")
    else:
        console.print(
            "[red]! No custom templates[/red]. Using built-in templates."
        )

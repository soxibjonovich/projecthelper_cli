from typing import Literal
from projecthelpercli.spec import ProjectSpec
from projecthelpercli.services import filesystem, renderer, template_loader
import typer
from rich.console import Console

app = typer.Typer()
console = Console()
err_console = Console(stderr=True)


@app.command()
def init(
    project_type: Literal["bot", "api"],
    project_title: str,
):
    spec = ProjectSpec(project_title=project_title, project_type=project_type)

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
        console.print("[green]✓[/green] Custom templates found.")
    else:
        console.print("[yellow]![/yellow] No custom templates. Using built-in templates.")


if __name__ == "__main__":
    app()

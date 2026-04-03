import subprocess
from typing import Annotated, Literal

import typer
from rich.console import Console

from projecthelpercli.services import features, filesystem, renderer, template_loader
from projecthelpercli.spec import FeatureName, ProjectSpec

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
        str, typer.Option("--version", "-v", help="Project version")
    ] = "1.0.0",
    project_features: Annotated[
        list[FeatureName] | None,
        typer.Option("--features", "-f", help="Features"),
    ] = None,
):
    spec = ProjectSpec(
        project_title=project_title,
        project_type=project_type,
        project_description=project_description,
        project_version=project_version,
        features=project_features or [],
    )

    try:
        project_dir = filesystem.create_project_dir(spec)
    except FileExistsError as e:
        err_console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)

    created = renderer.render_templates(spec, project_dir)
    for path in created:
        console.print(f"  [dim]→[/dim] {path.name}")

    try:
        features.execute_features(project_dir, spec)
    except subprocess.CalledProcessError as e:
        err_console.print(f"[red]Error:[/red] Feature '{e.cmd[0]}' failed: {e.stderr}")
        raise typer.Exit(1)

    console.print(f"\n[green]✓[/green] [bold]'{spec.project_title}'[/bold] created.")


@app.command()
def validate():
    if template_loader.check_templates():
        console.print("[green]✓ Custom templates found.[/green]")
    else:
        console.print(
            "[yellow]![/yellow] No custom templates. Using built-in templates."
        )


if __name__ == "__main__":
    app()

import typer
from sug import sug as sug_internal

app = typer.Typer()


@app.command()
def sug(
    name: str,
    working_dir: str,
    exec_start: str,
    bin_path: str,
    user: str,
    group: str,
    description: str = "",
    service_type: str = "simple",
):
    typer.echo(
        sug_internal(
            name,
            working_dir,
            exec_start,
            bin_path,
            user,
            group,
            description,
            service_type,
        )
    )


if __name__ == "__main__":
    app()

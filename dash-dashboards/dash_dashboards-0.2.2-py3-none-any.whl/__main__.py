import click

from .commands import generate_assets_cmd, start_dash, start_project


@click.group()
def cli():
    pass


cli.add_command(start_project)
cli.add_command(start_dash)
cli.add_command(generate_assets_cmd)

if __name__ == "__main__":
    cli()  # pragma: no cover

"""Console script for scitweet."""

import click


@click.command()
def main():
    """Main entrypoint."""
    click.echo("scitweet")
    click.echo("=" * len("scitweet"))
    click.echo("Package for scientific Twitter analysis")


if __name__ == "__main__":
    main()  # pragma: no cover

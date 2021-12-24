import click
from scrummy.rollover import rollover_todo


@click.group()
def cli():
    pass


@cli.command()
def rollover():
    rollover_todo()


if __name__ == '__main__':
    cli()

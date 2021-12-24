__version__ = "0.1.0"

import json
import logging
import os
import sys
from dataclasses import dataclass, field
from typing import List, Optional

import click
from prettytable import PrettyTable

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


@dataclass
class Config:
    database: str = ""
    dest_database: str = ""
    host = "localhost"
    port = 5432
    user = "postgres"
    m_factor = 1.0
    tables: Optional[List[str]] = field(default_factory=list)
    password = "postgres"
    owner: Optional[str] = None
    verbose = False
    drop = True


pass_config = click.make_pass_decorator(Config, ensure=True)


def _analyze_to_json(structure, fields, outpath, src_db_name, gen_db_name):
    filepath = os.path.join(outpath, f"analyze {src_db_name} {gen_db_name}.json")
    outdict = {"structure": structure, "fieldnames": fields}
    with open(filepath, "w+", encoding="UTF-8") as file:
        json.dump(outdict, file)
    return filepath


def _analyze_to_html(structure, fields, outpath, src_db_name, gen_db_name):
    output = ""
    for tablename, data in structure.items():
        output += f"<h2>{tablename}</h2>\n"
        if isinstance(data, str):
            output += data + "<br>\n"
        else:
            tbl = PrettyTable()
            tbl.field_names = ["column"] + fields
            for key in sorted(data.keys()):
                tbl.add_row(data[key])
            output += tbl.get_html_string() + "\n"

    htmlheader = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>pgsynthdata analyze</title>
<style>
    body{
    font-family: Helvetica, Arial, sans-serif;
    }
    th {
        background: #CCC
    }
    tr:nth-child(even) {
        background: #ECECEC
    }
    td {
    white-space: nowrap; 
    overflow: hidden;
    text-overflow: ellipsis;
    }
    table{
    width: 100%;
    table-layout: fixed;
    }
    table, th, td {
        border: 1px solid black;
        border-collapse: collapse;
    }
</style>
</head>
<body>
"""
    htmlfooter = """</body>
</html>"""
    filepath = os.path.join(outpath, f"analyze {src_db_name} {gen_db_name}.html")
    with open(filepath, "w+", encoding="UTF-8") as file:
        file.write(htmlheader)
        file.write(
            f"<h1>Analye database '{src_db_name}' (source) and '{gen_db_name}' (generated)</h1>"
        )
        file.write(output)
        file.write(htmlfooter)
    return filepath


@click.group()
@click.argument("database")
@click.option("-v", "--verbose", is_flag=True, default=False)
@click.option("-h", "--host", default="localhost", help="Host of the Database")
@click.option(
    "-p", "--port", default=5432, type=int, help="Port of the Database (default 5432)"
)
@click.option(
    "-u", "--user", default="postgres", help="User of the Database (default postgres)"
)
@click.option(
    "-t",
    "--tables",
    type=str,
    default="",
    help="Name(s) of table(s) to be filled, separated by : (default: all tables)",
)
@click.password_option(prompt=True, confirmation_prompt=False)
@pass_config
def cli(
    config: Config,
    database: str,
    verbose: bool,
    host: str,
    port: int,
    user: str,
    tables: str,
    password: str,
):
    config.database = database
    config.verbose = verbose
    config.host = host
    config.user = user
    config.port = port
    config.tables = tables.split(":") if tables else None
    config.password = password
    if verbose:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.WARNING)


@cli.command()
@pass_config
def show(config: Config):
    logging.info(f"Show database {config.database}")
    from .main import show as show_main

    structure = show_main(config)
    out = "" if structure else f"Nothing to show for '{config.database}'"
    for table in structure.values():
        out += "*******************************************\n"
        out += f"{table.pg_info.name} ({table.pg_info.schema}): {table.rows_to_generate} rows\n"
        tbl = PrettyTable()
        tbl.field_names = [
            "attname",
            "is_fk",
            "unique",
            "nullable",
            "data_type",
            "udt_name",
            "generator",
            "comment",
        ]
        for attname, col in table.columns.items():
            tbl.add_row(
                [
                    attname,
                    col.constraints.is_fk,
                    col.constraints.is_unique,
                    col.pg_info.is_nullable,
                    col.pg_info.data_type,
                    col.pg_info.udt_name,
                    col.generator.function.__name__
                    if col.generator
                    else "NO GENERATOR FOUND",
                    col.pg_comment[:25] + (col.pg_comment[25:] and "..")
                    if col.pg_comment
                    else "",
                ]
            )
        tbl.align = "l"
        out += tbl.get_string() + "\n\n"
    click.echo(out)


@cli.command()
@click.argument("dest_database")
@click.option("--format", type=click.Choice(["html", "json"], case_sensitive=False))
@pass_config
def analyze(config: Config, dest_database: str, format: str):
    logging.info(f"Analyze database {config} (generating {format})")
    config.dest_database = dest_database
    from .main import analyze as analyze_main

    structure, fields = analyze_main(config)

    filepath = ""
    if format == "json":
        filepath = _analyze_to_json(
            structure, fields, os.getcwd(), config.database, config.dest_database
        )
    else:  # HINT Default "html"
        filepath = _analyze_to_html(
            structure, fields, os.getcwd(), config.database, config.dest_database
        )
    click.echo(f"Analyze file created: {filepath}")


@cli.command()
@click.argument("dest_database")
@click.option(
    "-d",
    "--drop",
    is_flag=True,
    default=False,
    help="Drop destination database if exists",
)
@click.option("-o", "--owner", default="postgres", help="Owner of the new Database")
@click.option(
    "-m",
    "--m_factor",
    default=1.0,
    type=float,
    help="Multiplication factor for the generated synthetic data (default: 1.0)",
)
@pass_config
def generate(
    config: Config,
    dest_database: str,
    drop: bool,
    owner: str,
    m_factor: float,
):
    logging.info(f"Generate database {config.database} in {dest_database}")
    config.dest_database = dest_database
    config.owner = owner
    config.drop = drop
    config.m_factor = m_factor
    from .main import generate as generate_main

    click.echo(f"Start generating database '{config.dest_database}'")
    generate_main(config)
    click.echo(f"Finish generating database '{config.dest_database}'")


if __name__ == "__main__":
    cli()

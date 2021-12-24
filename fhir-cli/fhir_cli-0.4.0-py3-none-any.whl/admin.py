import getpass
import glob
from typing import Iterator
from uuid import NAMESPACE_DNS, uuid5

import requests
from psycopg2 import connect, sql

from fhir_cli import (
    CONNECT_CONFIG_TEMPLATE,
    CONNECT_URL,
    DBT_INIT_DB_TEMPLATE,
    DBT_META_TABLE,
    DBT_SCHEMA,
    FHIR_DBT_SCHEMA,
    FUNCTIONS_DIR_NAME,
    JINJA_ENV,
    POSTGRES_DB,
    POSTGRES_HOST,
    POSTGRES_PASSWORD,
    POSTGRES_PORT,
    POSTGRES_SERVER_NAME,
    POSTGRES_USER,
    PROJECT_DB,
    PROJECT_NAME,
    SOURCE_DB,
    SOURCE_HOST,
    SOURCE_PASSWORD,
    SOURCE_PORT,
    SOURCE_TYPE,
    SOURCE_USER,
)


def get_user_defined_functions() -> Iterator[str]:
    for file_path in glob.iglob(f"{FUNCTIONS_DIR_NAME}/**/*.sql", recursive=True):
        with open(file_path, "r") as f:
            yield f.read()


class Admin:
    """The admin command is used by an administrator to initialize a new project"""

    @staticmethod
    def createdb():
        """Create a new db for the project"""
        conn = connect(
            host=POSTGRES_HOST,
            dbname=POSTGRES_DB,
            port=POSTGRES_PORT,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
        )
        conn.autocommit = True

        role_stmt = sql.SQL("CREATE ROLE {role}").format(role=sql.Identifier(PROJECT_DB))
        db_stmt = sql.SQL("CREATE DATABASE {database}").format(database=sql.Identifier(PROJECT_DB))
        with conn.cursor() as curs:
            curs.execute(role_stmt)
            curs.execute(db_stmt)

        conn.close()

    @staticmethod
    def initdb():
        """Initialize the new db for the project"""
        conn = connect(
            host=POSTGRES_HOST,
            dbname=PROJECT_DB,
            port=POSTGRES_PORT,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
        )
        conn.autocommit = True

        project_id = uuid5(NAMESPACE_DNS, PROJECT_NAME)
        initdb_stmt = JINJA_ENV.get_template(DBT_INIT_DB_TEMPLATE).render(
            dbt_schema=DBT_SCHEMA,
            dbt_meta_table=DBT_META_TABLE,
            project_id=project_id,
            role=PROJECT_DB,
        )

        with conn.cursor() as curs:
            curs.execute(initdb_stmt)
            set_search_path_stmt = sql.SQL("SET search_path TO {dbt_schema}").format(
                dbt_schema=sql.Identifier(DBT_SCHEMA)
            )
            curs.execute(set_search_path_stmt)
            for func_definition in get_user_defined_functions():
                curs.execute(func_definition)
        conn.close()

    @staticmethod
    def connect():
        """Add a Kafka Connect connector"""
        connector = JINJA_ENV.get_template(CONNECT_CONFIG_TEMPLATE).render(
            project_db=PROJECT_DB,
            postgres_server_name=POSTGRES_SERVER_NAME,
            postgres_port=POSTGRES_PORT,
            postgres_user=POSTGRES_USER,
            postgres_password=POSTGRES_PASSWORD,
            schemas=",".join([FHIR_DBT_SCHEMA]),
        )
        r = requests.post(
            f"{CONNECT_URL}/connectors/",
            data=connector,
            headers={"Content-Type": "application/json"},
        )
        r.raise_for_status()

    @staticmethod
    def createuser(user: str, password: str = None):
        """Add a new user to the project

        Args:
            user (str): a username of choice
            password (:obj:`str`, optional): a password of choice. If not specified,
            the command will prompt for a password
        """

        while not password:
            password = getpass.getpass()

        conn = connect(
            host=POSTGRES_HOST,
            dbname=POSTGRES_DB,
            port=POSTGRES_PORT,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
        )
        conn.autocommit = True

        stmt = sql.SQL("CREATE USER {user} WITH PASSWORD %s IN ROLE {role}").format(
            user=sql.Identifier(user), role=sql.Identifier(PROJECT_DB)
        )
        with conn.cursor() as curs:
            curs.execute(stmt, (password,))

        conn.close()

    @staticmethod
    def link(source: str, target: str = None):
        """Create a foreign schema from a schema of the source database

        This command uses a foreign data wrapper that can be used to access data
        stored in an external server. The module opens a connection and extracts
        a database schema. Subsequently a user can import the data to the local
        database by creating a table or a materialized view selecting from a
        foreign table of a given schema.

        Args:
            source (str): the source schema
            target (:obj:`str`, optional): the target schema
        """
        if not target:
            target = source

        conn = connect(
            host=POSTGRES_HOST,
            dbname=PROJECT_DB,
            port=POSTGRES_PORT,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
        )
        conn.autocommit = True

        stmt = JINJA_ENV.get_template(f"{SOURCE_TYPE}_fdw.sql.j2").render(
            source_db=SOURCE_DB,
            source_host=SOURCE_HOST,
            source_port=SOURCE_PORT,
            source_user=SOURCE_USER,
            source_password=SOURCE_PASSWORD,
            project_db=PROJECT_DB,
            source_schema=source,
            target_schema=target,
        )
        with conn.cursor() as curs:
            curs.execute(stmt)

        conn.close()

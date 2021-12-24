import dataclasses
import logging
import os
import tempfile
from dataclasses import dataclass, field
from subprocess import PIPE, Popen
from typing import Any, Dict, Iterable, List, Optional, Tuple, no_type_check

import psycopg2
import psycopg2.extensions
import psycopg2.extras
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


@dataclass
class ColumnPgInfo:
    table_catalog: str = ""
    table_schema: str = ""
    table_name: str = ""
    column_name: str = ""
    ordinal_position: int = 0
    column_default: str = ""
    is_nullable: str = ""
    data_type: str = ""
    character_maximum_length: int = 0
    character_octet_length: int = 0
    numeric_precision: int = 0
    numeric_precision_radix: int = 0
    numeric_scale: int = 0
    datetime_precision: int = 0
    interval_type: str = ""
    interval_precision: int = 0
    character_set_catalog: str = ""
    character_set_schema: str = ""
    character_set_name: str = ""
    collation_catalog: str = ""
    collation_schema: str = ""
    collation_name: str = ""
    domain_catalog: str = ""
    domain_schema: str = ""
    domain_name: str = ""
    udt_catalog: str = ""
    udt_schema: str = ""
    udt_name: str = ""
    scope_catalog: str = ""
    scope_schema: str = ""
    scope_name: str = ""
    maximum_cardinality: int = 0
    dtd_identifier: str = ""
    is_self_referencing: str = ""
    is_identity: str = ""
    identity_generation: str = ""
    identity_start: str = ""
    identity_increment: str = ""
    identity_maximum: str = ""
    identity_minimum: str = ""
    identity_cycle: str = ""
    is_generated: str = ""
    generation_expression: str = ""
    is_updatable: str = ""


@dataclass
class ColumnPgStats:
    schemaname: str = ""
    tablename: str = ""
    attname: str = ""
    inherited: bool = False
    null_frac: float = 0
    avg_width: int = 0
    n_distinct: float = 0
    most_common_vals: List[Any] = field(default_factory=list)  # anyarray
    most_common_freqs: List[Any] = field(default_factory=list)  # ARRAY
    histogram_bounds: List[Any] = field(default_factory=list)  # anyarray
    correlation: float = 0
    most_common_elems: List[Any] = field(default_factory=list)  # anyarray
    most_common_elem_freqs: List[Any] = field(default_factory=list)  # ARRAY
    elem_count_histogram: List[Any] = field(default_factory=list)  # ARRAY


@dataclass
class TablePgInfo:
    schema: str = ""
    name: str = ""
    rowcount: int = 0
    rank: int = 0


_default_cursor_factory = psycopg2.extras.DictCursor


class Database:
    def __init__(self, dbname, user, password, host, port):
        self._dbname = dbname
        self._user = user
        self._pw = password
        self._host = host
        self._port = port
        self._open_connection()
        self._init_anyarray_extension()

    def __del__(self):
        self._close_connection()

    def _init_anyarray_extension(self):
        oid = self._execute_fetchone(
            "SELECT oid FROM pg_type WHERE typname='anyarray'"
        )["oid"]
        psycopg2.extensions.register_type(
            psycopg2.extensions.new_array_type((oid,), "anyarray[]", psycopg2.STRING)
        )

    def _execute(self, query, params=None):
        with self._conn.cursor() as cur:
            try:
                cur.execute(query, params)
            except Exception as ex:
                logging.error(
                    f"Exception with Statusmessage '{cur.statusmessage}' on query: {cur.query}"
                )
                raise ex

    def _execute_fetchall(
        self, query, params=None, cursor_factory=_default_cursor_factory
    ):
        with self._conn.cursor(cursor_factory=cursor_factory) as cur:
            try:
                cur.execute(query, params)
            except Exception as ex:
                logging.error(
                    f"Exception with Statusmessage '{cur.statusmessage}' on query: {cur.query}"
                )
                raise ex
            return cur.fetchall()

    def _execute_fetchone(
        self, query, params=None, cursor_factory=_default_cursor_factory
    ):
        result = self._execute_fetchall(query, params, cursor_factory)
        if len(result) > 0:
            return result[0]
        return None

    def _open_connection(self):
        logging.info(
            f"connect to database '{self._dbname}' on host '{self._host}:{self._port}' with user '{self._user}'"
        )
        try:
            self._conn = psycopg2.connect(
                dbname=self._dbname,
                user=self._user,
                password=self._pw,
                host=self._host,
                port=self._port,
            )
            self._conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        except psycopg2.OperationalError as ex:
            errmsg = (
                ex.pgerror
                if ex.pgerror
                else "Please check the database name, user and password"
            )
            logging.error(
                f"exception while connecting to database '{self._dbname}' on host '{self._host}:{self._port}' with user '{self._user}': {errmsg})"
            )
            raise ex

    def _close_connection(self):
        logging.info(
            f"close connection to database {self._dbname} on host {self._host}:{self._port} with user {self._user}"
        )
        if hasattr(self, "_conn") and not self._conn.closed:
            self._conn.close()

    def drop_database(self, db_name):
        try:
            self._execute(
                sql.SQL("DROP DATABASE {db_name}").format(
                    db_name=sql.Identifier(db_name)
                )
            )
        except psycopg2.DatabaseError as error:
            raise Exception(
                f"Database {db_name} could not be dropped: {error}"
            ) from error

    def create_database(self, db_name, owner=None):
        try:
            if owner is not None:
                self._execute(
                    sql.SQL("CREATE DATABASE {db_name} OWNER {owner}").format(
                        db_name=sql.Identifier(db_name), owner=sql.Identifier(owner)
                    )
                )
            else:
                self._execute(
                    sql.SQL("CREATE DATABASE {db_name}").format(
                        db_name=sql.Identifier(db_name)
                    )
                )
        except psycopg2.DatabaseError as error:
            raise Exception(
                f"Failed to create database {db_name}, Error: {error}"
            ) from error

    def does_db_exist(self, db_name):
        exists = self._execute_fetchone(
            "SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s", [db_name]
        )
        return exists is not None

    def create_destination_database(self, db_name, drop, owner=None):
        logging.info("Check if destination database exists")
        exists = self.does_db_exist(db_name)

        if exists and drop:
            logging.info("try to drop existing database")
            self.drop_database(db_name)
        elif exists and not drop:
            raise Exception(
                f"Database '{db_name}' already exists (use -d/--drop to delete an existing database if it already exists.)"
            )

        logging.info("Create destination database")
        self.create_database(db_name, owner)

    def get_connection_url(self):
        return f"postgresql://{self._user}:{self._pw}@{self._host}:{self._port}/{self._dbname}"

    def analyze(self):
        logging.info("Analyze Database with 'VACUUM ANALYZE'")
        self._execute("VACUUM ANALYZE;")
        logging.info("Finished with 'VACUUM ANALYZE'")

    def get_tables(self) -> List[TablePgInfo]:
        get_tabels_sql = """
        SELECT 
            nspname AS schema,
            relname as name
        FROM 
            pg_class C
        LEFT JOIN 
            pg_namespace N 
                ON (N.oid = C.relnamespace)
        WHERE 
            nspname = 'public'
            AND relkind='r' 
        ORDER BY name;
        """
        tables = [TablePgInfo(**t) for t in self._execute_fetchall(get_tabels_sql)]
        for table in tables:
            query = sql.SQL("SELECT count(*) as rowcount FROM {tablename}").format(
                tablename=sql.Identifier(table.name),
            )
            table.rowcount = self._execute_fetchone(query)["rowcount"]
        return tables

    def get_relations(self):
        get_releations_sql = """
        SELECT 
            tc.table_name AS "tablename",
            array_agg(ccu.table_name) AS "depends_on"
        FROM 
            information_schema.table_constraints AS tc 
        JOIN 
            information_schema.constraint_column_usage AS ccu
                ON ccu.constraint_name = tc.constraint_name
                AND ccu.table_schema = tc.table_schema
        WHERE
            constraint_type = 'FOREIGN KEY'
        GROUP BY 
	        tc.table_name
        """
        return self._execute_fetchall(get_releations_sql)

    def get_constraints(self):
        get_constraint_sql = """
        SELECT 
            kcu.column_name AS foreign_column,
            tc.table_name AS foreign_table,   
            ccu.column_name "referenced_primary_column",
            ccu.table_name AS "referenced_primary_table",
            tc.constraint_type,
            kcu.constraint_name		
        FROM 
            information_schema.table_constraints AS tc 
        JOIN 
            information_schema.key_column_usage AS kcu
                ON tc.constraint_name = kcu.constraint_name
                AND tc.table_schema = kcu.table_schema
        JOIN 
            information_schema.constraint_column_usage AS ccu
                ON ccu.constraint_name = tc.constraint_name
                AND ccu.table_schema = tc.table_schema
        """
        return self._execute_fetchall(get_constraint_sql)

    def get_column_infos(self, table_name) -> List[ColumnPgInfo]:
        get_column_infos_sql = _fill_fields_with_class_fields(
            sql.SQL(
                """
                SELECT
                    {fields}
                FROM
                    information_schema.columns
                WHERE
                    table_name = %s
                ORDER BY
                    ordinal_position;
                """
            ),
            ColumnPgInfo,
        )
        return [
            ColumnPgInfo(**c)
            for c in self._execute_fetchall(
                get_column_infos_sql,
                [table_name],
            )
        ]

    def get_stats(self, table_name, column_name=None):
        get_stats_sql = _fill_fields_with_class_fields(
            sql.SQL(
                """
                SELECT
                    {fields}
                FROM
                    pg_stats
                WHERE
                    schemaname = 'public'
                    AND tablename = %s
                """
            ),
            ColumnPgStats,
        )
        if column_name:
            get_stats_sql += sql.SQL("AND attname = %s")
            result = self._execute_fetchone(get_stats_sql, [table_name, column_name])
            return ColumnPgStats(**result) if result else None

        return [
            ColumnPgStats(**c)
            for c in self._execute_fetchall(get_stats_sql, [table_name])
        ]

    def get_column_comment(self, table_name, column_name):
        query = """
            SELECT
                (
                    SELECT
                        pg_catalog.col_description(c.oid, cols.ordinal_position::int)
                    FROM pg_catalog.pg_class c
                    WHERE
                        c.oid     = (SELECT cols.table_name::regclass::oid) AND
                        c.relname = cols.table_name
                ) as column_comment
            
            FROM information_schema.columns cols
            WHERE
                cols.table_catalog = %s 
                AND cols.table_name    = %s
                AND cols.column_name   = %s;
        """
        res = self._execute_fetchone(query, [self._dbname, table_name, column_name])
        if res:
            res = res["column_comment"]
        return res

    def run_statistic_query(self, query_str: str, table_name, column_name):
        query = sql.SQL(query_str).format(
            table_name=sql.Identifier(table_name),
            column_name=sql.Identifier(column_name),
            table_name_str=sql.Placeholder("table_name"),
            column_name_str=sql.Placeholder("column_name"),
        )

        return self._execute_fetchall(
            query, dict(table_name=table_name, column_name=column_name)
        )

    def insert_data(self, tablename: str, data: Dict[str, Optional[Iterable[Any]]]):
        data = {k: v for k, v in data.items() if v is not None}
        data_for_insert = [dict(zip(data, t)) for t in zip(*data.values())]
        sql_query, template = _create_insert_query(tablename, data.keys())
        with self._conn.cursor() as cur:
            try:
                psycopg2.extras.execute_values(
                    cur, sql_query, data_for_insert, template=template
                )
            except Exception as ex:
                logging.error(
                    f"Exception with Statusmessage '{cur.statusmessage}' on query: {cur.query}"
                )
                raise ex


def _fill_fields_with_class_fields(query: sql.SQL, class_or_instance) -> sql.SQL:
    return query.format(
        fields=sql.SQL(",").join(
            map(
                sql.Identifier,
                [
                    f.name
                    for f in dataclasses.fields(class_or_instance)
                    if f.name[:1] != "_"
                ],
            ),
        )
    )


def copy_database(
    from_db: Database,
    to_db: Database,
    path_to_dump_file=tempfile.NamedTemporaryFile(delete=False).name,
):
    from_connection_str = from_db.get_connection_url()
    to_connection_str = to_db.get_connection_url()
    logging.info("Copy database Structure")

    try:
        logging.info("Create Database Dump")
        dump_database(from_connection_str, path_to_dump_file)

        logging.info("Import Database Dump")
        import_database(to_connection_str, path_to_dump_file)

    except Exception as ex:
        raise Exception(f"Failed to copy Database structure: {ex}") from ex

    finally:
        if os.path.exists(path_to_dump_file):
            os.remove(path_to_dump_file)


def dump_database(connection_str: str, path_to_dump_file: str):
    with Popen(
        [
            "pg_dump",
            f"--dbname={connection_str}",
            "-sFc",
            "-f",
            f"{path_to_dump_file}",
        ],
        stdout=PIPE,
    ) as process:
        process.wait()
        return process.returncode


def import_database(connection_str: str, path_to_dump_file: str):
    with Popen(
        [
            "pg_restore",
            f"--dbname={connection_str}",
            f"{path_to_dump_file}",
        ],
        stdout=PIPE,
    ) as process:
        process.wait()
        return process.returncode


def _create_insert_query(
    tablename: str, colum_names: Iterable[str]
) -> Tuple[sql.SQL, sql.SQL]:
    sqlquery: sql.SQL = sql.SQL("INSERT INTO {tablename} ({fields}) VALUES %s").format(
        tablename=sql.Identifier(tablename),
        fields=sql.SQL(",").join(map(sql.Identifier, colum_names)),
    )
    template: sql.SQL = sql.SQL("({placeholders})").format(
        placeholders=sql.SQL(",").join(map(sql.Placeholder, colum_names)),
    )
    return sqlquery, template


@no_type_check
def empty_column_pg_infos() -> ColumnPgInfo:
    nones = [None for _ in dataclasses.fields(ColumnPgInfo)]
    return ColumnPgInfo(*nones)


@no_type_check
def empty_column_pg_stats() -> ColumnPgStats:
    nones = [None for _ in dataclasses.fields(ColumnPgStats)]
    return ColumnPgStats(*nones)


@no_type_check
def simple_column_pg_infos(data_type, udt_name=None) -> ColumnPgInfo:
    pg_info = empty_column_pg_infos()
    pg_info.data_type = data_type
    pg_info.udt_name = udt_name
    return pg_info

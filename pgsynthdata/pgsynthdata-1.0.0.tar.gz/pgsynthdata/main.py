import logging
import sys
from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional, Set, Union

from psycopg2.extras import DictRow
from toposort import toposort

from .database import (
    ColumnPgInfo,
    Database,
    TablePgInfo,
    copy_database,
    empty_column_pg_stats,
)
from .datagenerator import (
    Constraints,
    Generator,
    StatisticQuery,
    Statistics,
    get_generator,
)


@dataclass
class Config:
    database: str = ""
    dest_database: str = ""
    host = "localhost"
    port = 5432
    user = "postgres"
    m_factor = 1.0
    tables: List[str] = field(default_factory=list)
    password = "postgres"
    owner: Optional[str] = None
    verbose = False
    drop = True


@dataclass
class Column:
    pg_info: ColumnPgInfo
    pg_comment: str
    constraints: Constraints
    generator: Optional[Generator]
    stats: Statistics


@dataclass
class Table:
    pg_info: TablePgInfo
    rows_to_generate: int
    columns: Dict[str, Column] = field(default_factory=dict)


DbStructure = Dict[str, Table]

_STD_QUERIES = []


def show(config: Config) -> str:
    try:

        logging.info("connect to source database")
        src_db = Database(
            config.database, config.user, config.password, config.host, config.port
        )
        return _get_database_structure(src_db, config)
    except Exception as ex:
        logging.error(f"Can not show {config.database}, failed with exception: {ex}")
        sys.exit(1)


def analyze(config: Config) -> Dict[str, Union[str, Dict[str, Any]]]:
    try:
        logging.info(f"start analyze '{config.database}'' and '{config.dest_database}'")
        src_db = Database(
            config.database, config.user, config.password, config.host, config.port
        )
        dest_db = Database(
            config.dest_database, config.user, config.password, config.host, config.port
        )
        src_db = _get_database_structure(src_db, config)
        dest_db = _get_database_structure(dest_db, config)

        output = {}
        # HINT pg_stats fields to include
        fields = [
            "null_frac",
            "n_distinct",
            "most_common_vals",
            "most_common_freqs",
            "histogram_bounds",
            "most_common_elems",
            "most_common_elem_freqs",
            "elem_count_histogram",
        ]
        for tablename, table in src_db.items():
            tbl = {}
            output[tablename] = tbl
            for colname, col in table.columns.items():
                if (
                    col.stats.pg_stats
                    and dest_db.get(tablename)
                    and dest_db[tablename].columns.get(colname)
                    and dest_db[tablename].columns[colname].stats.pg_stats
                ):

                    tbl[colname] = [colname] + [
                        col.stats.pg_stats.__dict__[k] for k in fields
                    ]
                    tbl[colname + " (gen)"] = [colname + " (gen)"] + [
                        dest_db[tablename].columns[colname].stats.pg_stats.__dict__[k]
                        for k in fields
                    ]

                else:
                    output[
                        tablename
                    ] = f"No pg_stats for '{tablename}.{colname}' either in source or generated"

        return output, fields
    except Exception as ex:
        logging.error(f"analyze failed with exception: {ex}")
        sys.exit(1)


def generate(config: Config):
    try:
        logging.info("connect to source database")
        src_db = Database(
            config.database, config.user, config.password, config.host, config.port
        )
        logging.info("create destination database")
        src_db.create_destination_database(
            config.dest_database, config.drop, config.owner
        )
        logging.info("connect to destination database")
        dest_db = Database(
            config.dest_database, config.user, config.password, config.host, config.port
        )
        logging.info("copy schema to destination database")
        copy_database(src_db, dest_db)

        tables = _get_database_structure(src_db, config)
        relations = src_db.get_relations()
        for level in _toposort_and_filter_table_relations(
            relations, tables, config.tables
        ):
            for tablename in level:
                logging.info(f"generate data for table '{tablename}'")
                data = _generate_data(tables, tablename)
                logging.info(f"insert data in table '{tablename}'")
                dest_db.insert_data(tablename, data)
        logging.info("finish generate database")
    except Exception as ex:
        logging.error(
            f"Can not generate {config.dest_database}, failed with exception: {ex}"
        )
        sys.exit(1)


def _generate_data(
    tables: DbStructure, tablename: str
) -> Dict[str, Optional[Iterable[Any]]]:
    table = tables[tablename]
    generated_data: Dict[str, Optional[Iterable[Any]]] = {}
    for col_name, col in table.columns.items():
        if col.stats and col.stats.pg_stats.inherited:
            break  # HINT no need to generate inherited data
        if table.rows_to_generate == 0:
            logging.warning(
                f"skipping table '{tablename}'' because it does not contain any data (rows_to_generate=0)"
            )
            return generated_data
        if col.generator:
            generated_data[col_name] = col.generator.function(
                col.stats, col.pg_info, col.constraints, table.rows_to_generate
            )
            for foreign_table, foreign_column in col.constraints.used_as_fk_by:
                tables[foreign_table].columns[
                    foreign_column
                ].constraints.fk_values = generated_data[col_name]

        else:
            if col.pg_info.is_nullable:
                generated_data[col_name] = None
                logging.warning(
                    f"no generator found table '{tablename}' and column '{col_name}'. No data will be generated for this column"
                )
            else:
                logging.error(
                    f"no generator found table '{tablename}' and column '{col_name}' and is not NOT NULLABLE. Therefore, it most likely fail to INSERT the data"
                )

    return generated_data


def _get_database_structure(database: Database, config: Config) -> Dict[str, Table]:
    database.analyze()
    tables: Dict[str, Table] = {}
    raw_constraints = database.get_constraints()

    for table_info in database.get_tables():
        tablename = table_info.name
        rows_to_generate = int(table_info.rowcount * config.m_factor)
        table = Table(pg_info=table_info, rows_to_generate=rows_to_generate)
        tables[tablename] = table
        for column_info in database.get_column_infos(tablename):
            columnname = column_info.column_name

            # constraints
            constraints = _create_column_constraints(
                raw_constraints, tablename, columnname
            )

            # comment
            pg_comment = database.get_column_comment(tablename, columnname)

            # generator
            generator = get_generator(column_info, constraints, pg_comment)

            # statistics
            pg_stats = database.get_stats(tablename, columnname)
            if not pg_stats:
                pg_stats = empty_column_pg_stats()
            std_stats = _run_statistics_queries(
                _STD_QUERIES, database, tablename, columnname
            )
            custom_stats = custom_stats = (
                _run_statistics_queries(
                    generator.custom_queries, database, tablename, columnname
                )
                if generator and generator.custom_queries
                else None
            )
            stats = Statistics(pg_stats, std_stats, custom_stats)

            # column info & contraints
            column = Column(
                pg_info=column_info,
                constraints=constraints,
                pg_comment=pg_comment,
                generator=generator,
                stats=stats,
            )
            table.columns[columnname] = column

    return tables


def _run_statistics_queries(
    queries: list[StatisticQuery], database: Database, tablename: str, columnname: str
):
    results = {}
    for query in queries:
        results[query.name] = database.run_statistic_query(
            query.query, tablename, columnname
        )
    return results


def _toposort_and_filter_table_relations(
    relations: List[DictRow],
    all_tables: DbStructure,
    filter_tables: Union[List[str], None] = None,
):
    relations_dict: Dict[str, Set] = {key: set() for key in all_tables.keys()}

    for table in relations:
        relations_dict[table["tablename"]] = set(table["depends_on"][1:-1].split(","))

    if filter_tables:
        # all depends_on must be in filter_table list for all tables in filter_table
        if not all(
            all(t in filter_tables for t in relations_dict[ft]) for ft in filter_tables
        ):
            raise Exception(
                "table filter is not applicable because of given relations of the tables"
            )

        relations_dict = {k: v for k, v in relations_dict.items() if k in filter_tables}

    return list(toposort(relations_dict))


def _create_column_constraints(pg_constraints, tablename, columnname):
    used_as_fk_by = [
        (c["foreign_table"], c["foreign_column"])
        for c in pg_constraints
        if c["referenced_primary_column"] == columnname
        and c["referenced_primary_table"] == tablename
        and c["constraint_type"] != "PRIMARY KEY"
        and c["constraint_type"] != "UNIQUE"
    ]

    is_unique = any(
        c["referenced_primary_column"] == columnname
        and c["referenced_primary_table"] == tablename
        and (c["constraint_type"] == "PRIMARY KEY" or c["constraint_type"] == "UNIQUE")
        for c in pg_constraints
    )

    is_fk = any(
        c["foreign_column"] == columnname and c["foreign_table"] == tablename
        for c in pg_constraints
        if c["constraint_type"] == "FOREIGN KEY"
    )

    return Constraints(
        is_unique=is_unique,
        used_as_fk_by=used_as_fk_by,
        is_fk=is_fk,
    )

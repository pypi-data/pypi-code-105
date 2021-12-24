import os
import re
from taostd import td
from jinja2 import Template
from taostd.model import SqlModel
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

_SQL_CONTAINER = dict()


def init_db(database, pool_size=2, tz_offset=8, mapper_path='mapper', default_dynamic=False, *args, **kwargs):
    _load_sql(mapper_path, default_dynamic)
    td.init_db(database, pool_size, tz_offset, *args, **kwargs)


def get(sql_id: str, **kwargs):
    sql = get_named_sql(sql_id, **kwargs)
    return td.get(sql)


def select_one(sql_id: str, **kwargs):
    sql = get_named_sql(sql_id, **kwargs)
    return td.select_one(sql)


def select(sql_id: str, **kwargs):
    sql = get_named_sql(sql_id, **kwargs)
    return td.select(sql)


def execute(sql_id: str, params=None, **kwargs) -> int:
    """
    simple execute SQL and return affected rows.
    params is not None, execute insert sql by prepare statement. like: insert into meters(?,?,?);
    :param sql_id: SQL id
    :param params: parameters by taos.new_bind_params() function created
    :return: affected rows: int
    """
    sql = get_named_sql(sql_id, **kwargs)
    return td.execute(sql, params)


def insert_one(table: str, **kwargs):
    return td.insert_one(table, **kwargs)


def insert_one_with_stable(table: str, stable: str, **kwargs):
    return td.insert_one_with_stable(table, stable, **kwargs)


def insert_many(table: str, args: list, batch_size=100):
    return td.insert_many(table, args, batch_size)


def insert_many_with_stable(table: str, stable: str, args: list, batch_size=100):
    return td.insert_many_with_stable(table, stable, args, batch_size)


def insert_many_tables(args: list, batch_size=100):
    return td.insert_many_tables(args, batch_size)


def drop_table(table: str):
    td.drop_table(table)


def get_named_sql(sql_id, **kwargs):
    sql_model = _get_sql_model(sql_id)
    return sql_model.sql.render(**kwargs) if sql_model.dynamic else sql_model.sql


def _get_sql_model(sql_id):
    global _SQL_CONTAINER
    sql_model = _SQL_CONTAINER.get(sql_id)
    if sql_model:
        return sql_model
    else:
        raise KeyError(f"invalid sql id: {sql_id}.")


def _get_path(path):
    if path.startswith("../"):
        rpath = ''.join(re.findall("../", path))
        os.chdir(rpath)
        path = path[len(rpath):]
    elif path.startswith("./"):
        path = path[2:]
    return os.path.join(os.getcwd(), path)


def _load_sql(path, default_dynamic):
    if not os.path.isabs(path):
        path = _get_path(path)

    for f in os.listdir(path):
        file = os.path.join(path, f)
        if os.path.isfile(file) and f.endswith(".xml"):
            _read_mapper(file, default_dynamic)
        elif os.path.isdir(file):
            _load_sql(file, default_dynamic)


def _read_mapper(file, default_dynamic):
    global _SQL_CONTAINER
    tree = ET.parse(file)
    root = tree.getroot()
    namespace = root.attrib.get('namespace', '')
    for child in root:
        key = namespace + "." + child.attrib.get('id')
        dynamic = child.attrib.get('dynamic')
        if (dynamic and dynamic.lower() == 'true') or default_dynamic:
            _SQL_CONTAINER[key] = SqlModel(sql=Template(child.text), dynamic=True)
        else:
            _SQL_CONTAINER[key] = SqlModel(sql=child.text)


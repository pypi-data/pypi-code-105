from typing import final, Dict, List
from hashlib import md5
import re

from .Core import core


class Rules:
    """BAse rules for data"""
    def __init__(self):
        self.__rules = {
            "type_int": {
                "min": 0,
                "max": 255,
                "valide_foo": self.valid_int
            },
            "type_text": {
                "length": 100,
                "valide_foo": self.valid_text
            },
            "type_bool": {
                "symbols": [True, False, 1, 0],
                "valide_foo": self.valid_bool
            },
            "type_date": {
                "do": re.search,
                "valide_foo": self.valid_date
            }
        }
        self.user_rules = {}

    def get_rules(self):
        """Return current rules"""
        return self.__rules

    def get_user_rules(self):
        """Return user rules"""
        return self.user_rules

    def new_rules(self, rules: dict):
        """Create new rules(user rules)"""
        self.user_rules = rules
        return self.user_rules

    def valid_int(self, int_val, rule):
        """Validate int"""
        if rule["min"] < int_val < rule["max"]:
            return True
        return False

    def valid_text(self, text_val, rule):
        """Validate text"""
        if len(text_val) <= rule["length"]:
            return True
        return False

    def valid_bool(self, bool_val, rule):
        """Validate bool"""
        if bool_val in rule["symbols"]:
            return True
        return False

    def valid_date(self, date_val, rule):
        """Validate data"""
        res = rule["do"]("[0-9]{4}-[0-9]{2}-[0-9]{2}", str(date_val))

        if res is not None and res.span()[1] == 10:
            return True

        return False


class ORMType:
    """Base type class"""
    # @staticmethod
    def _is_valid_datas(self, user_rules: Rules):
        if user_rules == "*":
            rules = Rules()
            rule = rules.get_rules()[self.type_name]

            return (rule["valide_foo"](self.value, rule), rule)

        rule = user_rules.get_user_rules()[self.type_name]

        return (rule["valide_foo"](self.value, rule), rule)


class Int(ORMType):
    """
        SQL    - INT
        Python - int
    """
    def __init__(self, value):
        self.type_name = "type_int"
        self.value = value


class Text(ORMType):
    """
        SQL    - TEXT
        Python - str
    """
    def __init__(self, value):
        self.type_name = "type_text"
        self.value = value


class Bool(ORMType):
    """
        SQL    - BOOL
        Python - bool
    """
    def __init__(self, value):
        self.type_name = "type_bool"
        self.value = value


class Date(ORMType):
    """
        SQL    - DATE
        Python - datetime.today()
    """
    def __init__(self, value):
        self.type_name = "type_date"
        self.value = value


class AutoField(ORMType):
    """
        SQL    - SERIAL PRIMARY KEY
        Python - int
    """
    def __init__(self, value=""):
        self.type_name = "type_int"
        self.value = value


class BasicTypes:
    """Contains all available types"""
    TYPES_LIST = (Int, Text, Bool, Date, AutoField)
    DB_TYPES_LIST = {
        Int: "INT", Text: "TEXT",
        Bool: "BOOL", Date: "DATE",
        AutoField: "SERIAL PRIMARY KEY"
    }


class Column:
    """Field of table"""
    def __init__(self, column_type, column_name):
        self.__column_type = column_type
        self.__column_name = column_name
        self.__column_sql_type = BasicTypes.DB_TYPES_LIST.get(
            self.__column_type
        )

    @property
    def type(self):
        """Return orm-type of the column"""
        return self.__column_type

    @property
    def name(self):
        """Return name of the column"""
        return self.__column_name

    @property
    def sql_type(self):
        """Return sql-type of the column"""
        return self.__column_sql_type


@final
class TablesManager:
    """
        Give access to tables and accept to manipulate them
    """
    tables: Dict = {}
    Utables: Dict = {}

    @staticmethod
    def find_by_name(name):
        """Return one tablesby name of table"""
        return TablesManager.tables.get(md5(name.encode("utf-8")).digest())

    @staticmethod
    def find_one_by_column(*column_names):
        """Select one table by name of column"""
        count = len(column_names)

        for table in TablesManager.tables.values():
            for column in table.columns:
                if column.name in column_names:
                    count -= 1

                if count == 0:
                    return table

            count = len(column_names)
        return False

    @staticmethod
    def find_many_by_column(*column_names):
        """Select all tables by name of column"""
        tables = []
        count = len(column_names)

        for table in TablesManager.tables.values():
            for column in table.columns:
                if column.name in column_names:
                    count -= 1

                if count == 0:
                    tables.append(table)
                    break

            count = len(column_names)

        return tables

    @staticmethod
    def unite(*tables):
        """A function that returns multiple wrapped tables"""
        columns_u = []
        name_ = []
        for table in tables:
            for column in table.columns:
                if column.name not in columns_u:
                    columns_u.append(column)
            name_.append(table.name.lower())
        name_ = "U".join(name_)

        class UnatedTable(
            Table, metaclass=TableMeta, parent=Table,
            U_table_name=name_, U_table_columns=columns_u,
            U_tables = tables
        ):
            """Table which are few tables"""
            def __init__(self, name: str):
                self._is_unated = True
                self._parent_tables = tables

                TablesManager.Utables.update(
                    {
                        md5(self.name.encode("utf-8")).digest(): self
                    }
                )

        u_table = UnatedTable(name_)
        u_table.set_columns(*columns_u)

        u_table.set_columns = lambda x=None: print("Not allowed for united tables")

        return u_table


class Table:
    """Table of database"""
    def __init__(self, name: str):
        self.__name = name
        self.__columns: List[Column] = []
        TablesManager.tables.update(
            {
                md5(self.__name.encode("utf-8")).digest(): self
            }
        )

    @property
    def name(self):
        """Get name of the table"""
        return self.__name

    @property
    def columns(self):
        """Get columns of the table"""
        return self.__columns

    def set_columns(self, *names):
        """Set columns for table:
            .set_columns(Column(type of datas, name of column))
        """
        self.__columns = names

    def create(self, connection):
        """Will create table if not exist"""
        core.Create(self, BasicTypes.TYPES_LIST, connection)


class TableMeta(type):
    """Metaclass for Table, will create UnatedTable"""
    def __new__(cls, name, parents, namespace, **kwargs):
        parent_name: Table = kwargs["parent"](kwargs["U_table_name"])

        namespace.update(
            {
                "name": parent_name.name,
                "columns": kwargs["U_table_columns"],
                "set_columns": parent_name.set_columns,
                "tables": kwargs["U_tables"]
            }
        )
        return type(name, (), namespace)


class DataSet(object):
    """Will return data from database"""
    def __init__(self, table_name, columns, data):
        self.__table_name = table_name
        self.__columns = columns
        self.__data = data

    def get_column_names(self):
        """Return column names of table"""
        return self.__columns

    def get_data(self):
        """Return tuple of recved data"""
        return tuple(self.__data)

    def get_table_name(self):
        """Return table name"""
        return self.__table_name

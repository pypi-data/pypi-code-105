from .core import CheckDatas, SQLConditions
from ..types_ import DataSet

from .exceptions_ import SlashRulesError


class Insert():
    def __init__(self, conn, table, names, values, rules="*"):
        responce = self.__validate(table, names, values, rules)
        conn.execute(CheckDatas.checkSQL(responce, "insert"))

    def __validate(self, table, names, values, rules):
        CheckDatas.checkStr(table.name)

        for name in names:
            CheckDatas.checkStr(name)

        for value in values:
            if value.type_name == "type_text":
                CheckDatas.checkStr(value.value)

            valid_responce = value._is_valid_datas(rules)
            # value._is_valid_datas(rules)
            if not valid_responce[0]:
                raise SlashRulesError(f"\n\n\nRule: {valid_responce[1]}")

        names = str(names)
        names = names.replace("(", "")
        names = names.replace(")", "").replace("'", "")
        sql_responce = f"""INSERT INTO {table.name} ({names}) VALUES ("""

        for index, val in enumerate(values):
            if val.type_name == "type_int":
                sql_responce += str(val.value)
                if (index + 1) != len(values):
                    sql_responce += ", "
            elif val.type_name == "type_text":
                sql_responce += ("'" + val.value + "'")
                if (index + 1) != len(values):
                    sql_responce += ","
            elif val.type_name == "type_bool":
                sql_responce += str(val.value)
                if (index + 1) != len(values):
                    sql_responce += ", "
            elif val.type_name == "type_date":
                sql_responce += ("'" + str(val.value) + "'")
                if (index + 1) != len(values):
                    sql_responce += ", "
        sql_responce += ")"

        return sql_responce


class Delete():
    def __init__(self, conn, table, condition: SQLConditions):
        responce = self.__validate(table, condition)
        conn.execute(CheckDatas.checkSQL(responce, "delete"))

    def __validate(self, table, condition):
        CheckDatas.checkStr(table.name)
        sql_responce = f"DELETE FROM {table.name}{condition}"

        return sql_responce


class Select():
    def __init__(self, conn, table, names, condition: SQLConditions):
        self.__conn = conn
        self.__responce = self.__validate(table, names, condition)
        self.__table__name = table.name
        self.__names = names

    def __validate(self, table, names, condition):
        CheckDatas.checkStr(table.name)

        return "SELECT {} FROM {}{}".format(
            ", ".join([n for n in names]),
            table.name, condition
        )

    def get(self):
        self.__conn.execute(CheckDatas.checkSQL(self.__responce, "select"))

        return DataSet(
            self.__table__name, self.__names, self.__conn.fetchall()
        )


class Update():
    def __init__(self, conn, table, names, values, condition, rules="*"):
        responce = self.__validate(table, names, values, condition, rules)
        conn.execute(CheckDatas.checkSQL(responce, "update"))

    def __validate(self, table, names, values, condition, rules):
        CheckDatas.checkStr(table.name)
        sql_responce = "UPDATE {} SET ".format(table.name)

        for index, value in enumerate(values):
            valid_responce = value._is_valid_datas(rules)
            if not valid_responce[0]:
                raise SlashRulesError(f"\n\n\nRule: {valid_responce[1]}")

            if value.type_name == "type_text":
                sql_responce += " = ".join((names[index], f"'{value.value}'"))
            elif value.type_name == "type_int":
                sql_responce += " = ".join((names[index], f"{value.value}"))
            elif value.type_name == "type_bool":
                sql_responce += " = ".join((names[index], f"{value.value}"))
            elif value.type_name == "type_date":
                sql_responce += " = ".join((names[index], f"'{value.value}'"))

            sql_responce += ", " if index != (len(values) - 1) else ""

        sql_responce += condition

        return sql_responce


class Operations():
    def __init__(self, connection):
        self.__connection = connection

    def insert(self, table, names, values, *, rules="*"):
        try:
            table._is_unated
        except AttributeError:
            if rules == "*":
                Insert(self.__connection, table, names, values)
            else:
                Insert(self.__connection, table, names, values, rules)

    def select(self, table, names, condition=" "):
        try:
            table._is_unated
            # что-то будет
        except AttributeError:
            return Select(self.__connection, table, names, condition).get()

    def delete(self, table, condition=" "):
        try:
            table._is_unated
        except AttributeError:
            return Delete(self.__connection, table, condition)

    def update(self, table, column_names, values, condition=" "):
        try:
            table._is_unated
        except AttributeError:
            Update(self.__connection, table, column_names, values, condition)

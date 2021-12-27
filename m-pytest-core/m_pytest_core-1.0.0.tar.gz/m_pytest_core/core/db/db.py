from os import getenv

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, ARRAY, BIGINT, BigInteger, BINARY, BLOB, Boolean, CHAR, CLOB, Date, \
    DateTime, DECIMAL, Enum, Float, Integer, Interval, JSON, LargeBinary, NCHAR, Numeric, NVARCHAR, PickleType, REAL, \
    SmallInteger, String, Text, Time, TIMESTAMP, TypeDecorator, Unicode, UnicodeText, VARBINARY, VARCHAR
from sqlalchemy.dialects.oracle import RAW, VARCHAR2

BASE = declarative_base()


class DB:
    def __init__(self, session=None):
        self.session = session
        self.connection = None

    def _connection(self, environment):
        engine = None
        environment['DB']['USER'] = getenv("DB_USER")
        environment['DB']['PASSWORD'] = getenv("DB_PASSWORD")

        if environment['DB']['DB_TYPE'].lower() == 'postgresql':
            engine = create_engine(f"postgresql://{environment['DB']['USER']}:{environment['DB']['PASSWORD']}@"
                                   f"{environment['DB']['HOST']}:{environment['DB']['PORT']}/"
                                   f"{environment['DB']['DB_NAME']}")
        elif environment['DB']['DB_TYPE'].lower() == 'mysql':
            engine = create_engine(
                f"mysql://{environment['DB']['USER']}:{environment['DB']['PASSWORD']}@{environment['DB']['HOST']}/"
                f"{environment['DB']['DB_NAME']}")
        elif environment['DB']['DB_TYPE'].lower() == 'oracle':
            engine = create_engine(
                f"oracle://{environment['DB']['USER']}:{environment['DB']['PASSWORD']}@{environment['DB']['HOST']}:"
                f"{environment['DB']['PORT']}/?service_name={environment['DB']['DB_NAME']}&mode=2"
            )
        elif environment['DB']['DB_TYPE'].lower() == 'mssql':
            engine = create_engine(f"mssql+pyodbc://{environment['DB']['USER']}:{environment['DB']['PASSWORD']}@"
                                   f"{environment['DB']['DB_NAME']}")
        elif environment['DB']['DB_TYPE'].lower() == 'sqlite':
            engine = create_engine(f"sqlite:///{environment['DB']['PATH']}")

        return engine

    def create_session(self, environment):
        self.connection = self._connection(environment=environment)
        Session = sessionmaker(self.connection)
        BASE.metadata.create_all(self.connection)
        return Session()

    def get(self, table_name: any, limit: int = 0, offset: int = 0):
        try:
            if limit and not offset:
                result = self.session.query(table_name).limit(limit).all()
            elif limit and offset:
                result = self.session.query(table_name).limit(limit).offset(offset).all()
            else:
                result = self.session.query(table_name).all()
            items = []
            for row in result:
                tmp = {}
                for _row in vars(row):
                    if _row not in ['_sa_instance_state']:
                        tmp[_row] = row.__dict__[_row]
                items.append(tmp)
            return items
        except BaseException as e:
            print(e.args)
            return False

    def create(self, query_object: any):
        try:
            self.session.add(query_object)
            self.session.commit()
            return {'id': query_object.id}
        except BaseException as e:
            print(e.args)
            self.session.rollback()
            return False

    def create_all(self, query_object: any):
        try:
            self.session.add_all(query_object)
            self.session.commit()
            ids = []
            for item in query_object:
                ids.append(item.id)
            return {'ids': ids}
        except BaseException as e:
            print(e.args)
            self.session.rollback()
            return False

    def update(self, table_name: any, condition: dict, update_value: dict):
        try:
            self.session.query(table_name).filter_by(**condition).update(update_value)
            self.session.commit()
            return 'Successful updated'
        except BaseException as e:
            print(e.args)
            self.session.rollback()
            return False

    def delete(self, table_name: any, condition: dict):
        try:
            self.session.query(table_name).filter_by(**condition).delete()
            self.session.commit()
            return 'Successful deleted'
        except BaseException as e:
            print(e.args)
            self.session.rollback()
            return False

    def execute(self, query: str):
        """
            execute("SELECT * FROM user WHERE id=5")
            :param query: str
            :return:
        """
        try:
            result = self.session.execute(query)
            self.session.commit()
            items = []
            for row in result:
                items.append(row)
            return items
        except BaseException as e:
            print(e.args)
            self.session.rollback()
            return False

    def get_by(self, table_name: any, condition: dict, limit: int = 0, offset: int = 0):
        try:
            if limit and not offset:
                result = self.session.query(table_name).filter_by(**condition).limit(limit).all()
            elif limit and offset:
                result = self.session.query(table_name).filter_by(**condition).limit(limit).offset(offset).all()
            else:
                result = self.session.query(table_name).filter_by(**condition).all()
            items = []
            for row in result:
                tmp = {}
                for _row in vars(row):
                    if _row not in ['_sa_instance_state']:
                        tmp[_row] = row.__dict__[_row]
                items.append(tmp)
            return items
        except BaseException as e:
            print(e.args)
            return False

    def close(self):
        self.session.close()
        self.connection.dispose()


class DBHelper:
    def column(self, column, dimensions=1, *args, **kwargs):
        """
        :param column:
            array, biging, giginteger, binary,
            blob, bool, char, clob, date,
            datetime, decimal, emum, float,
            int, interval, json, largebinary,
            nchar, numeric, nvarchar, pickletype,
            real, smallint, str, text, time,
            timestamp, typedecoder, unicode,
            unicodetext, varbinary, varchar
        :param dimensions: 1
        :return: поле типа SQL
        """
        column_type = {
            'array': ARRAY,
            'biging': BIGINT,
            'giginteger': BigInteger,
            'binary': BINARY,
            'blob': BLOB,
            'bool': Boolean,
            'char': CHAR,
            'clob': CLOB,
            'date': Date,
            'datetime': DateTime,
            'decimal': DECIMAL,
            'emum': Enum,
            'float': Float(dimensions),
            'int': Integer,
            'interval': Interval,
            'json': JSON,
            'largebinary': LargeBinary,
            'nchar': NCHAR,
            'numeric': Numeric,
            'nvarchar': NVARCHAR,
            'pickletype': PickleType,
            'real': REAL,
            'smallint': SmallInteger,
            'str': String(dimensions),
            'text': Text(dimensions),
            'time': Time,
            'timestamp': TIMESTAMP,
            'typedecoder': TypeDecorator,
            'unicode': Unicode,
            'unicodetext': UnicodeText,
            'varbinary': VARBINARY,
            'varchar': VARCHAR(dimensions),
            'varchar2': VARCHAR2(dimensions),
            'raw': RAW(dimensions),
        }.get(column, 'varchar')

        return Column(column_type, *args, **kwargs)

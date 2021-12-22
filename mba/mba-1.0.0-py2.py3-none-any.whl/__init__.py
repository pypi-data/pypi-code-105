import sqlalchemy
from sqlalchemy import create_engine
from mba.config.core import config

def db_connection(username=config.app_config.db_username, password=config.app_config.db_password, database=config.app_config.db_schema, db_host=config.app_config.db_host, db_port=config.app_config.db_port):
    # global conn
    engine = create_engine(sqlalchemy.engine.url.URL.create(
            "mysql+pymysql", username=username,
            password=password,
            database=database,
            host=db_host,
            port=db_port))
    conn = engine.connect()
    return conn

# try:
#     db_connection = db_connection()
# except:
#     raise Exception(f"Try Initialize Connection")

print('-'*20, 'from init', '-'*20)
import logging

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

global connection
connection = db_connection()


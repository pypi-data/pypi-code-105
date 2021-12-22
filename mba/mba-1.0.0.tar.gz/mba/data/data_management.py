import joblib
import pandas as pd
from pathlib import Path
import sqlalchemy
from sqlalchemy import create_engine

# from mba import __version__ as _version
from mba.config.core import DATASET_DIR, TRAINED_MODEL_DIR, config


class DataFlow(object):
    def __init__(self):
        pass

    def read_data_csv(self, file_name: str) -> pd.DataFrame:
        dataframe = pd.read_csv(Path(f"{DATASET_DIR}/external/{file_name}"))
        return dataframe

    def read_processed_data_pkl(self, file_name: str):
        data = joblib.load(Path(f"{DATASET_DIR}/processed/{file_name}"))
        return data

    def connect_to_mysql(self):
        engine = create_engine(sqlalchemy.engine.url.URL.create(
            "mysql+pymysql", username=config.app_config.db_username,
            password=config.app_config.db_password,
            database=config.app_config.db_schema,
            host=config.app_config.db_host,
            port=config.app_config.db_port))
        conn = engine.connect()
        return conn

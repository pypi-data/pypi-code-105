import os, psycopg2
import pandas.io.sql as psql
from hydroplane.data_sources.postgres.postgres_tables import DATA_SOURCES_TABLE, QUERIES_TABLE, CARDS_TABLE, PAGES_TABLE, COLLECTIONS_TABLE, LOGS_TABLE, SETTINGS_TABLE



class HydroPostgres:
    def __init__(self, host, port, database, user, password):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password

    def postgres_create_connection(self):
        conn = psycopg2.connect(host=self.host, port=self.port, database=self.database, user=self.user, password=self.password)
        return conn


    def postgres_close_connection(self, conn):
        conn.close()   


    def postgres_create_table(self, conn, tbl_name, tbl_sql):  
        cur = conn.cursor()
        cur.execute(tbl_sql)  
        conn.commit() 
        log_type = "INFO"
        log_msg = "TABLE: " + tbl_name + " - Acitve"
        # self.postgres_add_log(conn, log_type, log_msg)


    def postgres_add_log(self, conn, log_type, log_msg):
        cur = conn.cursor()
        # CREATE LOGS TABLE IF IT DOES NOT EXIST 
        self.postgres_create_table(conn, "LOGS", LOGS_TABLE)
        # ADD LOG 
        log_timestamp = ""
        log_sql = '''INSERT INTO logs (log_timestamp, log_type, log_msg) VALUES ('{log_timestamp}', '{log_type}', '{log_msg}')'''.format(log_timestamp=log_timestamp, log_type=log_type, log_msg=log_msg) 
        cur.execute(log_sql)  
        conn.commit() 


DATA_SOURCES_TABLE = """
                    CREATE TABLE IF NOT EXISTS data_sources (
                        data_source_id SERIAL PRIMARY KEY,
                        data_source_name varchar(40) UNIQUE NOT NULL,
                        data_source_endpoint varchar(100) NOT NULL,
                        data_source_port varchar(8) NOT NULL,
                        data_source_type varchar(20) NOT NULL
                    )
                    """

QUERIES_TABLE = """
                CREATE TABLE IF NOT EXISTS queries (
                    query_id SERIAL PRIMARY KEY,
                    query_name varchar(40) UNIQUE NOT NULL, 
                    query_data_source_name varchar(40) NOT NULL,
                    query_object varchar(60) NOT NULL,
                    query_object_dimensions json NOT NULL
                )
                """


CARDS_TABLE = """
                CREATE TABLE IF NOT EXISTS cards (
                    card_id SERIAL PRIMARY KEY,
                    card_name varchar(40) UNIQUE NOT NULL,  
                    card_type varchar(40) NOT NULL,
                    card_query varchar(40) NOT NULL,
                    card_chart_type varchar(40) NOT NULL,
                    card_chart_dimensions json NOT NULL,
                    card_tbl_dimensions json NOT NULL
                )
                """

PAGES_TABLE = """
                CREATE TABLE IF NOT EXISTS pages (
                    page_id SERIAL PRIMARY KEY,
                    page_name varchar(40) UNIQUE NOT NULL,  
                    page_endpoint varchar(40) NOT NULL, 
                    page_card_layout json NOT NULL
                )
                """

COLLECTIONS_TABLE = """
                    CREATE TABLE IF NOT EXISTS collections (
                        collection_id SERIAL PRIMARY KEY,
                        collection_name varchar(40) UNIQUE NOT NULL,  
                        collection_icon varchar(40) NOT NULL, 
                        collection_pages json NOT NULL
                    )
                    """

# FIX TIMESTAMP
LOGS_TABLE = """
                    CREATE TABLE IF NOT EXISTS logs (
                        log_id SERIAL PRIMARY KEY,
                        log_timestamp varchar(40) UNIQUE NOT NULL,  
                        log_type varchar(40) UNIQUE NOT NULL,  
                        log_msg varchar(40) NOT NULL 
                    )
                    """


SETTINGS_TABLE = """
                    CREATE TABLE IF NOT EXISTS settings (
                        settings_id SERIAL PRIMARY KEY,
                        retention_period INTEGER UNIQUE NOT NULL 
                    )
                    """
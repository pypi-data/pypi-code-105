from simple_ddl_parser import DDLParser

ddl =  """
       
CREATE TABLE public.accounts (
    user_id integer NOT NULL,
    username character varying(50) NOT NULL,
    password character varying(50) NOT NULL,
    email character varying(255) NOT NULL,
    created_on timestamp without time zone NOT NULL,
    last_login timestamp without time zone
);
ALTER TABLE IF EXISTS public.accounts
    ADD CONSTRAINT accounts_username_key UNIQUE (username);
       """
result = DDLParser(ddl).run(group_by_type=True, output_mode="bigquery")
import pprint

pprint.pprint(result)

import os
from afs2datasource import DBManager, constant

# --------- config --------- #
db_type = constant.DB_TYPE['SQLSERVER']
username = 'sa'
password = 'yourStrongPassword!'
host = '61.219.26.30'
port = 1433
database = 'TestDB'
table_name = 'customers'

# -------------------------- #

manager = DBManager(db_type=db_type,
    username=username,
    password=password,
    host=host,
    port=port,
    database=database,
    querySql=''
)

try:
  # connect to MySQL
  is_success = manager.connect()
  print('Connection: {}'.format(is_success))

  # check if table is exist
  is_table_exist = manager.is_table_exist(table_name)

  # Query record
  querySql = 'SELECT * FROM {}'.format(table_name)
  print('Execute Query: {}'.format(querySql))
  data = manager.execute_query(querySql)
  print(data)

  # Delete row
  condition = 'passenger_id = 1'
  print('Delete Row with condition: {}'.format(condition))
  is_success = manager.delete_record(table_name=table_name, condition=condition)
  print('Delete Row: {}'.format(is_success))
  
  # Check if successed
  if is_success:
    querySql = 'SELECT * FROM {table_name}'.format(
      table_name=table_name
    )
    data = manager.execute_query(querySql)
    if len(data):
      raise ValueError('Delete Row Failed')
    else:
      print('Delete Row Successfully')

  manager.disconnect()

except Exception as e:
  print(e)

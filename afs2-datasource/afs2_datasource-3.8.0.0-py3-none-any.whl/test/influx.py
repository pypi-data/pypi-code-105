
from afs2datasource import DBManager, constant
manager = DBManager(db_type=constant.DB_TYPE['INFLUXDB'],
  username='',
  password='',
  host='172.16.8.40',
  port=8086,
  database='datahub',
  querySql="select * from test"
)

manager.connect()
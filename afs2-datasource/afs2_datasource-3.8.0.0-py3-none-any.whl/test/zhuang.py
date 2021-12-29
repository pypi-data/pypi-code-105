from afs2datasource import DBManager, constant
db = DBManager(db_type=constant.DB_TYPE['POSTGRES'],
  username="84e4ea12-7f91-4c3a-a71e-bcec27c3bd31",
  password="o8p1gnf2eij6cpq061lc3gfhak",
  host="61.219.26.33",
  port=5432,
  database="015adab7-c646-48e4-9771-5352a4bdb29e",
  querySql="select * from db_iris.db_iris"
)

db.connect()
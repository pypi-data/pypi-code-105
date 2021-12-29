import os
from afs2datasource import DBManager, constant

# --------- config --------- #
db_type = constant.DB_TYPE['S3']
endpoint = 'http://61.219.26.12:8080' # S3 endpoint
access_key = '6704bed85c7f40deb3afceb9f4c56134' # S3 access key
secret_key = '6YGsRLdtcOuAueHbRWY9p5b8FCxQWpGT0'  # S3 secret key

bucket_name = 'stacy_test' # bucket name
source = 'test/titanic.csv' # 要上傳的檔案(local)
folder_name = 'test/'  # 上傳上去的folder name

# 會上傳 source 到 S3 bucket 裡面
# 一個在 /
# 一個在 /folder_name 下面
# 接著會下載這兩個檔案到local
# -------------------------- #

_, file_name = os.path.split('{}'.format(source))
destination = os.path.join(folder_name, file_name)
download_file = source
query = {
  'bucket': bucket_name,
  'blobs': {
    'files': [file_name],
    'folders': folder_name
  }
}

manager = DBManager(db_type=db_type,
  endpoint=endpoint,
  access_key=access_key,
  secret_key=secret_key,
  buckets=query
)

try:
  # connect to S3
  is_success = manager.connect()
  print('Connection: {}'.format(is_success))

  # check if bucket is exist
  is_table_exist = manager.is_table_exist(bucket_name)

  # create bucket
  if not is_table_exist:
    print('Create Container {0} successfully: {1}'.format(bucket_name, manager.create_table(bucket_name)))
  print('Container {0} exist: {1}'.format(bucket_name, manager.is_table_exist(bucket_name)))

  # insert file
  is_file_exist = manager.is_file_exist(bucket_name, file_name)
  print('File {0} is exist: {1}'.format(file_name, is_file_exist))
  if not is_file_exist:
    manager.insert(table_name=bucket_name, source=source, destination=file_name)
    print('Insert file {0} successfully: {1}'.format(source, manager.is_file_exist(bucket_name, file_name)))
    is_file_exist = manager.is_file_exist(bucket_name, destination)
  print('File {0} is exist: {1}'.format(destination, is_file_exist))

  is_file_exist = manager.is_file_exist(bucket_name, destination)
  print('File {0} is exist: {1}'.format(destination, is_file_exist))
  if not is_file_exist:
    manager.insert(table_name=bucket_name, source=source, destination=destination)
    print('Insert file {0} successfully: {1}'.format(source, manager.is_file_exist(bucket_name, destination)))
  is_file_exist = manager.is_file_exist(bucket_name, destination)
  print('File {0} is exist: {1}'.format(destination, is_file_exist))

  # download files
  if is_file_exist:
    response = manager.execute_query()
    print('Execute query successfully: {}'.format(response))

except Exception as e:
  print(e)

import os

# os.environ['PAI_DATA_DIR'] = 'eyJ0eXBlIjoiZGF0YWh1Yi1maXJlaG9zZSIsImRhdGEiOnsiY3JlZGVudGlhbCI6eyJ1cmkiOiJpbmZsdXhkYjovLzpAUEMwMzA0MDM6ODA4Ni9kYXRhaHViIiwidXNlcm5hbWUiOiJ1c2VybmFtZSIsInBhc3N3b3JkIjoicGFzc3dvcmQiLCJob3N0IjoiODA4NiIsImRhdGFiYXNlIjoiaW5mbHV4ZGI6Ly86QFBDMDMwNDAzOjgwODYvZGF0YWh1YiJ9LCJkYXRhaHViX2NvbmZpZyI6W3sibmFtZSI6ImRhdGFodWItMSIsInByb2plY3RfaWQiOiI0a3ZMSHdhOXdVd28iLCJub2RlX2lkIjoiZTkxOWM1NTItZjkzYS00ZDZjLTg3MWMtNzY5ODlhNGU0OGI4IiwiZGV2aWNlX2lkIjoiRGV2aWNlMSIsInRhZ3MiOlsiQVRhZzEiLCJBVGFnMiIsIlRUYWcyIl19XSwiZGF0YWh1Yl91cmwiOiJodHRwOi8vcG9ydGFsLWRhdGFodWItZGF0YWh1Yi1la3MwMDguc2Eud2lzZS1wYWFzLmNvbSIsImRhdGFodWJBdXRoIjoiWTJNdWVXRnVaMEJoWkhaaGJuUmxZMmd1WTI5dExuUjNPbU5qWVRoallXRXpRRk56TUE9PSIsInVzZXJuYW1lIjoiY2MueWFuZ0BhZHZhbnRlY2guY29tLnR3IiwidGltZUxhc3QiOnsibGFzdERheXMiOjEsImxhc3RIb3VycyI6MCwibGFzdE1pbnMiOjB9fX0='


from afs2datasource import DBManager, constant
manager = DBManager(db_type=constant.DB_TYPE['DATAHUB'],
  username='ssopassroot@email.com',  # sso username
  password='ToorSs@p0SS',  # sso password
  datahub_url='https://portal-datahub-ensaas.aifs.wise-paas.com',
  datahub_config=[{
    "name": "test0510", # dataset name
    "project_id": "afs-demo",#datahub的mongodb数据库中不会存这个参数
    "node_id": "90b016ce-d171-423b-b16f-2d2eeb82f49e",
    "device_id": "Device1",
    "tags": [
      "ATag0"
    ]
  }],
  uri='influxdb://d44b1476-f532-4ce2-8244-fec7bffd858e:0ERVNiAbxCBWJZldFT6JMHdr4@172.17.21.111:8086/1f65d529-898c-46d8-8d71-30671a3f820b',
  # timeRange or timeLast
  #timeRange=[{'start': start_ts, 'end': end_ts}],
  timeLast={'lastDays': 360, 'lastHours': 77, 'lastMins': 77}
)
manager.connect()
df = manager.execute_query()
print(df)
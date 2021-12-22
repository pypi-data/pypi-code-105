from client_app import publish_to_sub
import json

json_msg = {
  'topic': 'topic1',
  'content_format': 'json',
  'content': json.dumps({'name': 'susan', 'age': 78})
}

csv_msg = {
  'topic': 'topic1',
  'content_format': 'csv',
  'content': 'a,b,c\n1,2,3',
}

tsv_msg = {
  'topic': 'topic1',
  'content_format': 'tsv',
  'content': 'a\tb\tc\n1\t2\t3',
}

xml_object = """<?xml version="1.0" ?>
<person>
  <name>John</name>
  <age>20</age>
</person>
"""

xml_msg = {
  'topic': 'topic1',
  'content_format': 'xml',
  'content': xml_object,
}

messages = [json_msg]

publish_to_sub(
  host='localhost',
  port='10000',
  message=csv_msg,
  #messages=messages
)


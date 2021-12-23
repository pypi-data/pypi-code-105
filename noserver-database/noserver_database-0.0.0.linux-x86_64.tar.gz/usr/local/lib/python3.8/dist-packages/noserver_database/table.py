import json
import os.path
import secrets
from database.document import Document
from database.alert import DatabaseAlert, DatabaseError


class Table:

    def __init__(self, name, super_):
        self.table = super_.folder + '/' + name + '.json'
        self.super_ = super_
        if not os.path.isfile(self.table):
            if self.super_.debug:
                DatabaseAlert(f'Table \'{name}\' does not exist !', self.super_)
            else:
                raise DatabaseError(f'Table \'{name}\' does not exist !')

    def raw_json_data(self):
        return json.loads(open(self.table).read())['data']

    def insert_one(self, doc):
        data = self.raw_json_data()
        with open(self.table, 'w+') as f:
            doc['_id'] = secrets.token_urlsafe(16)
            data.append(doc)
            data = {'data': data}
            f.write(json.dumps(data))
            f.close()

    def find_one(self, doc: dict, order=1):
        data = self.raw_json_data()
        if order == -1:
            data.reverse()
        for document in data:
            for item in doc.keys():
                if item in document.keys():
                    if document[item] == doc[item]:
                        return Document(document, self.super_, self)
                    else:
                        continue
        return None

    def find(self, doc: dict, order=1):
        if doc == {}:
            return [Document(doc, self.super_, self) for doc in self.raw_json_data()]
        data = self.raw_json_data()
        if order == -1:
            data.reverse()
        documents = []
        for document in data:
            for item in doc.keys():
                if item in document.keys():
                    if document[item] == doc[item]:
                        documents.append(Document(document, self.super_, self))
                    else:
                        continue
        return documents

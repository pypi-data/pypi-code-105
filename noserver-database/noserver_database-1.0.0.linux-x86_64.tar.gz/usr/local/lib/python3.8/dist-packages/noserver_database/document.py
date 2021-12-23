import json
from database.alert import DatabaseAlert, DatabaseError


class Document:

    def __init__(self, data, super_, table_children):
        self.data = data
        self.super_ = super_
        self.table = table_children

    def __getitem__(self, item):
        if self.data is None and not self.super_.debug:
            raise DatabaseError('This document was deleted ! Cannot interact with him !')
        elif self.data is None and self.super_.debug:
            DatabaseAlert('This document was deleted ! Cannot interact with him !', self.super_)
        return self.data[item]

    def __str__(self):
        return str(self.data)

    def delete(self):
        if self.data is None and not self.super_.debug:
            raise DatabaseError('This document was already deleted ! Cannot interact with him !')
        elif self.data is None and self.super_.debug:
            DatabaseAlert('This document was already deleted ! Cannot interact with him !', self.super_)
        data = self.table.raw_json_data()
        with open(self.table.table, 'w+') as f:
            del data[data.index(self.data)]
            data = {'data': data}
            print(data)
            f.write(json.dumps(data))
            f.close()
            self.table = None
            self.data = None
            self.super_ = None
            return True

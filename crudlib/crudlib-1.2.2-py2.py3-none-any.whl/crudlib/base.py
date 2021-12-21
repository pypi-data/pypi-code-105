class DataBase:
    def query(self, tb, condition=None):
        raise NotImplementedError

    def insert_one(self, tb, doc):
        raise NotImplementedError

    def insert_many(self, tb, doc_list):
        raise NotImplementedError

    def update(self, tb, doc, condition):
        raise NotImplementedError
